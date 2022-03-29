#lang racket

;; 用cond实现基础的解释器和CPS形式，并测试并发执行

(require "lookup.rkt")
(require "concurrent.rkt")

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; 定义结构
(struct Function (params body))
(struct Closure (f envs))
(struct Built (f))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; 内置函数

(define (set-timeout envs arg-values)
  (let ([f (car arg-values)]
        [ms (cadr arg-values)])
    (let ([call-time (get-now-time)])  
      (schedule
       (lambda ()
         (let ([now (get-now-time)]
               [expire (+ call-time ms)])
           (if (< now expire)
               (set-timeout envs `(,f ,(- expire now)))
               (interp/call `(,f) (Closure-envs f)))))
       (make-task-label envs "set-timeout")
       100
       (lambda () ms)))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; 定义环境，结构:'(env1 (env2 (env3)))
(define empty-env empty-table)
(define add-env add-table)
(define lookup-env lookup-table)

;(define empty-env empty-bst)
;(define add-env add-bst)
;(define lookup-env lookup-bst)

(define (make-env keys values)
  (if (or
       (empty? keys)
       (empty? values))
      empty-env
      (let ([key (car keys)]
            [value (car values)]
            [rest-keys (cdr keys)]
            [rest-values (cdr values)])
        (add-env key value (make-env rest-keys rest-values)))))

(define (make-env/items items)
  (if (empty? items)
      empty-env
      (let* ([item (car items)]
             [rest-items (cdr items)]
             [key (car item)]
             [value (cdr item)])
        (add-env key value (make-env/items rest-items)))))

(define (extend-env new-env envs)
  (if (empty? envs)
      (list new-env)
      (append (list new-env) envs)))

(define empty-envs '())

(define (lookup-envs key envs)
  (if (empty? envs)
      (error "not found:" key)
      (let* ([current-env (car envs)]
             [rest-envs (cdr envs)]
             [result (lookup-env key current-env)])
        (if (not-found? result)
            (lookup-envs key rest-envs)
            result))))

; 初始环境
(define (make-init-envs items)
  (extend-env (make-env/items items) empty-env))

(define built-env
  (make-env/items (list
                   `(set-timeout . ,(Built set-timeout))
                   )))

(define init-envs
  (extend-env built-env
              (make-init-envs
               (list
                `(+ . ,+)
                `(- . ,-)
                `(* . ,*)
                `(/ . ,/)
                `(= . ,=)
                `(< . ,<)
                `(> . ,>)
                `(println . ,println)
                `(printf . ,printf)
                `(get-now-time . ,get-now-time)
                ))))

(define (add-task-env name env)
  (extend-env
   (make-env/items (list
                    `(task-id . ,name)
                    ))
   env))

; 测试环境
(define env0 '())
(define env1 (make-env
              '(a b c)
              '(1 2 3)))
(define env2 (make-env/items
              (list
               `(x . 10)
               `(y . 20))))
(define env3 (extend-env env2 (extend-env env1 env0)))
(define env4 (extend-env
              (make-env '(c) '(166))
              env3))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; map CPS
(define (mapCPS f ls k)
  (if (empty? ls)
      (k '())
      (let ([first (car ls)]
            [rest (cdr ls)])
        (f first
           (lambda (f-result)
             (mapCPS f rest
                     (lambda (rest-result)
                       (k (cons f-result rest-result)))))))))
        
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; 解释器
(define (interp exp envs)
  (cond
    [(self-valued? exp) exp]
    [(variable? exp) (lookup-envs (variable-name exp) envs)]
    [(special-form? exp) ((select-special-form-interp (special-form-label exp)) exp envs)]
    [else (interp/call exp envs)]))

; 解释器CPS
(define (interp/CPS exp envs k)
  (schedule
   (lambda ()
     (cond
       [(self-valued? exp) (k exp)]
       [(variable? exp) (k (lookup-envs (variable-name exp) envs))]
       [(special-form? exp) ((select-special-form-interp-cps (special-form-label exp)) exp envs k)]
       [else (interp/call/CPS exp envs k)]))
   (make-task-label envs "interp/CPS")
   100
   (lambda () exp)))

(define (make-task-label envs procedure-name)
  (string->symbol
   (string-append
    (symbol->string (lookup-envs 'task-id envs))
    " "
    procedure-name)))

; 自求值表达式
(define (self-valued? exp)
  (or
   (number? exp)
   (boolean? exp)
   (string? exp)
   (empty? exp)
   (Closure? exp)))

; 变量表达式
(define variable? symbol?)

(define (variable-name v)
  v)

; 解释lambda
(define (special-form-interp/lambda exp envs)
  ; 构造出闭包
  (let ([params (cadr exp)]
        [body (cddr exp)])
    (Closure
     (Function params body)
     envs)))

(define (make-ast/lambda params body)
  (append
   '(lambda)
   (list params)
   body))

; 解释lambda CPS
(define (special-form-interp/lambda/CPS exp envs k)
  ; 构造出闭包
  (let ([params (cadr exp)]
        [body (cddr exp)])
    (k (Closure
        (Function params body)
        envs))))

; 解释if
(define (special-form-interp/if exp envs)
  (let ([pred-exp (cadr exp)]
        [true-branch-exp (caddr exp)]
        [false-branch-exp (cadddr exp)])
    (let ([pred-value (interp pred-exp envs)])
      (if pred-value
          (interp true-branch-exp envs)
          (interp false-branch-exp envs)))))


; 解释if CPS
(define (special-form-interp/if/CPS exp envs k)
  (let ([pred-exp (cadr exp)]
        [true-branch-exp (caddr exp)]
        [false-branch-exp (cadddr exp)])
    (interp/CPS pred-exp envs
                (lambda (pred-value)
                  (if pred-value
                      (interp/CPS true-branch-exp envs k)
                      (interp/CPS false-branch-exp envs k))))))

; 解释let
(define (special-form-interp/let exp envs)
  ; 当做独立特性实现
  (let ([definitions (cadr exp)]
        [body (cddr exp)])
    (let ([keys (map car definitions)]
          [es (map cadr definitions)])
      (let ([values (map
                     (lambda (e) (interp e envs))
                     es)])
        (let ([local-envs (extend-env
                           (make-env keys values)
                           envs)])
          (last
           (map
            (lambda (e) (interp e local-envs))
            body)))))))

; 解释let
(define (special-form-interp/let/sugar exp envs)
  ; 当做语法糖
  (let ([definitions (cadr exp)]
        [body (cddr exp)])
    (let ([params (map car definitions)]
          [arg-exps (map cadr definitions)])
      (let ([sugar-function (make-ast/lambda params body)])
        (let ([sugar-call (make-ast/call sugar-function arg-exps)])
          (interp/call sugar-call envs))))))

; 解释let CPS
(define (special-form-interp/let/sugar/CPS exp envs k)
  ; 当做语法糖
  (let ([definitions (cadr exp)]
        [body (cddr exp)])
    (let ([params (map car definitions)]
          [arg-exps (map cadr definitions)])
      (let ([sugar-function (make-ast/lambda params body)])
        (let ([sugar-call (make-ast/call sugar-function arg-exps)])
          (interp/call/CPS sugar-call envs k))))))
                           
; 特殊形式表达式
(define (special-form? exp)
  (let ([label (special-form-label exp)])
    (in label special-form-labels)))

(define (in x ls)
  (if (empty? ls)
      #f
      (or
       (eq? x (car ls))
       (in x (cdr ls)))))

(define special-form-label car)

(define special-form-interps (list
                              `(lambda . ,special-form-interp/lambda)
                              `(if . ,special-form-interp/if)
                              `(let . ,special-form-interp/let/sugar)
                              ))

(define special-form-interps-cps (list
                                  `(lambda . ,special-form-interp/lambda/CPS)
                                  `(if . ,special-form-interp/if/CPS)
                                  `(let . ,special-form-interp/let/sugar/CPS)
                                  ))

(define (select label special-interps)
  (let ([result (assq label special-interps)])
    (if result
        (cdr result)
        (error "not found special interp:" label))))

(define (keys items) ; items是pair的list
  (map car items))

(define (values items) ; items是pair的list
  (map (cdr items)))

(define special-form-labels (keys special-form-interps))

(define (select-special-form-interp label)
  (select label special-form-interps))

(define (select-special-form-interp-cps label)
  (select label special-form-interps-cps))

; 解释call
(define (interp/call exp envs)
  (let* ([op-exp (car exp)]
         [arg-exps (cdr exp)]
         [op-value (interp op-exp envs)]       
         [arg-values (map
                      (lambda (arg-exp) (interp arg-exp envs))
                      arg-exps)])
    (cond
      [(Closure? op-value)  (let* ([f (Closure-f op-value)]
                                   [closure-envs (Closure-envs op-value)]
                                   [params (Function-params f)]
                                   [body (Function-body f)]
                                   [local-env (extend-env
                                               (make-env params arg-values)
                                               closure-envs)])
                              (last
                               (map
                                (lambda (body-exp) (interp body-exp local-env))
                                body)))
                            ]
      [(Built? op-value) (let ([f (Built-f op-value)])
                           (f envs arg-values))]
      
      ; 调用原生apply处理基础过程
      [else (apply op-value arg-values)])))

; 解释call CPS
(define (interp/call/CPS exp envs k)
  (let* ([op-exp (car exp)]
         [arg-exps (cdr exp)])
    (interp/CPS op-exp envs
                (lambda (op-value)
                  (mapCPS
                   (lambda (arg-exp k)
                     (interp/CPS arg-exp envs k))
                   arg-exps
                   (lambda (arg-values)
                     (cond
                       [(Closure? op-value)
                        (let* ([f (Closure-f op-value)]
                               [closure-envs (Closure-envs op-value)]
                               [params (Function-params f)]
                               [body (Function-body f)]
                               [local-env (extend-env
                                           (make-env params arg-values)
                                           closure-envs)])
                          (mapCPS
                           (lambda (body-exp k)
                             (interp/CPS body-exp local-env k))
                           body
                           (lambda (body-value) (k (last body-value)))))]
                       [(Built? op-value) (let ([f (Built-f op-value)])
                                            (k (f envs arg-values)))]                                            
                       [else 
                        (k (apply op-value arg-values))])))))))
                                                                                
(define (make-ast/call op-exp arg-exps)
  (append
   (list op-exp)
   arg-exps))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; 测试解释器

(define (interp1)
  (define code '(+ 2 3))
  (interp code init-envs)) ; => 5

(define (interp1/CPS)
  (define code '(+ 2 3))
  (interp/CPS code (add-task-env 't0 init-envs) println) ; => 5
  (task-loop))

(define (interp2)
  (define code '((lambda (x y) (+ (* x x) (* y y ))) 2 3))
  (interp code init-envs)) ; => 13

(define (interp2/CPS)
  (define code '((lambda (x y) (+ (* x x) (* y y ))) 2 3))
  (interp/CPS code (add-task-env 't0 init-envs) println) ; => 13
  (task-loop))

(define (interp3)
  (define code '(((lambda (x) (lambda (y) (* x y))) 2) 3))
  (interp code init-envs)) ; => 6

(define (interp3/CPS)
  (define code '(((lambda (x) (lambda (y) (* x y))) 2) 3))
  (interp/CPS code (add-task-env 't0 init-envs) println) ; => 6
  (task-loop))

(define (interp4)
  (define code '((lambda (x) (lambda (y) (+ x y))) 2))
  (define closure (interp code init-envs))
  (define running-envs (extend-env
                        (make-env/items (list
                                         `(x . 66)
                                         ))
                        init-envs))
  (interp/call `(,closure 100) running-envs)) ; => 102, not 166

(define (interp4/CPS)
  (define code '((lambda (x) (lambda (y) (+ x y))) 2))
  (interp/CPS code (add-task-env 't0 init-envs)
              (lambda (closure)
                (let ([running-envs (extend-env
                                     (make-env/items (list
                                                      `(x . 66)
                                                      ))
                                     init-envs)])
                  (interp/call/CPS `(,closure 100)
                                   (add-task-env 't0 running-envs)
                                   println)))) ; => 102, not 166
  (task-loop))

(define (interp5)
  (define code '(((lambda (x y)
                    (if (< x y)
                        (lambda (a b) (+ a b))
                        (lambda (c d) (* c d)))) 10 20) 15 15)) ; => 30
  (interp code init-envs))

(define (interp5/CPS)
  (define code '(((lambda (x y)
                    (if (< x y)
                        (lambda (a b) (+ a b))
                        (lambda (c d) (* c d)))) 10 20) 15 15)) ; => 30
  (interp/CPS code (add-task-env 't0 init-envs) println)
  (task-loop))

(define (interp6)
  (define code '(let ([x 2]
                      [y 3]
                      [z 100])
                  (let ([x (+ x x)] ; 4
                        [y (* y y)]); 9
                    (+ x x)
                    (+ y y)
                    (+ z x y)))) ; => 113
  (interp code init-envs))

(define (interp6/CPS)
  (define code '(let ([x 2]
                      [y 3]
                      [z 100])
                  (let ([x (+ x x)] ; 4
                        [y (* y y)]); 9
                    (+ x x)
                    (+ y y)
                    (+ z x y)))) ; => 113
  (interp/CPS code (add-task-env 't0 init-envs) println)
  (task-loop))

(define (interp7)
  (define code '(let ([f (lambda (x y)
                           (if (< x y)
                               (lambda (a b) (* a b))
                               (lambda (a b) (+ a b))))]
                      [x 100]
                      [y 200]
                      [a 16]
                      [b 16])
                  ((f x y) a b))) ; => 256
  (interp code init-envs))

(define (interp7/CPS)
  (define code '(let ([f (lambda (x y)
                           (if (< x y)
                               (lambda (a b) (* a b))
                               (lambda (a b) (+ a b))))]
                      [x 100]
                      [y 200]
                      [a 16]
                      [b 16])
                  ((f x y) a b))) ; => 256
  (interp/CPS code (add-task-env 't0 init-envs) println)
  (task-loop))

(define (interp8)
  (define code '(let ([x 2]
                      [y 3]
                      [z 100])
                  (let ([x (+ x x)] ; 4
                        [y (* y y)]); 9
                    (println "hello")
                    (println "world")
                    (+ z x y)))) ; => 113
  (interp code init-envs))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; 测试多任务调度

(define (interp/CPS/schedule-time)
  (define code1 '(((lambda (x y)
                     (if (< x y)
                         (lambda (a b) (+ a b))
                         (lambda (c d) (* c d)))) 10 20) 15 15)) ; => 30

  
  (define code2 '(let ([f (lambda (x y)
                            (if (< x y)
                                (lambda (a b) (* a b))
                                (lambda (a b) (+ a b))))]
                       [x 100]
                       [y 200]
                       [a 16]
                       [b 16])
                   ((f x y) a b))) ; => 256
  
  (use-concurrent-time)
  (init-time-piece 1)
  (init-global-time)
  (interp/CPS code1 (add-task-env 't1 init-envs) println)
  (interp/CPS code2 (add-task-env 't2 init-envs) println)
  (task-loop))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; 测试set-timeout触发任务调度

(define (interp8/set-timeout)
  (define code '(let ([time-gap-milliseconds 2])
                  
                  (set-timeout
                   (lambda ()
                     (printf "timestamp:~a, msg:~a~n" (get-now-time) "after timeout show this!"))
                   time-gap-milliseconds)  ; 2ms 后执行函数
                  
                  (printf "timestamp:~a, msg:~a~n" (get-now-time) "show this now!")))  ; 立刻执行
  
  (interp code (add-task-env 't1 init-envs))
  (task-loop))

  