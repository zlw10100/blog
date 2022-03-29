#lang racket

;; 用match实现基础的解释器和CPS形式，并测试并发执行

(require "lookup.rkt")
(require "concurrent.rkt")


(define (tree-sum tree)
  (match tree
    [(? number? x) x]
    [`(,e1 ,e2) (+
                 (tree-sum e1)
                 (tree-sum e2))]))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; CPS函数

(define (map/CPS f ls k)
  (if (empty? ls)
      (k '())
      (let ([first (car ls)]
            [rest (cdr ls)])
        (f first
           ; 这里假设了f是接受k的函数
           (lambda (first-result)
             (map/CPS f rest
                      (lambda (rest-results)
                        (k (cons first-result rest-results)))))))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; 结构定义
  
(struct Closure (params body env))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; 原子表达式

(define (variable? x)
  (symbol? x))

(define (self-valued? x)
  (or
   (number? x)
   (string? x)
   (boolean? x)
   (eq? x '())))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; 环境定义

(define add-env add-table)
(define lookup-env lookup-table)
(define empty-env empty-table)

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

(define (extend-env new-env env)
  (append new-env env))

(define init-env (list
                  `(+ . ,+)
                  `(- . ,-)
                  `(* . ,*)
                  `(/ . ,/)
                  `(< . ,<)
                  `(println . ,println)
                  ))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; 解释器

(define (interp exp env)
  (match exp
    [(? self-valued?) exp]
    [(? variable?) (let ([value (lookup-env exp env)])
                     (if (not-found? value)
                         (error "not found variable:" exp)
                         value))]

    ;; lambda表达式
    [(list 'lambda (list params ...) body ...) (Closure params body env)]

    ;; if表达式
    [(list 'if pred true-branch false-branch) (let ([pred-value (interp pred env)])
                                                (if pred-value
                                                    (interp true-branch env)
                                                    (interp false-branch env)))]
    ;; let表达式-语法糖
    [(list 'let (list items ...) body ...) (let* ([params (map car items)]
                                                  [args (map cadr items)]
                                                  [let-sugar (append
                                                              (list (append (list 'lambda params) body))
                                                              args)])
                                             (interp let-sugar env))]

    ;; let表达式-独立特性
    ;    [(list 'let (list items ...) body ...) (let* ([values (map (lambda (e) (interp e env)) (map cadr items))]
    ;                                                  [items-env (make-env (map car items) values)]
    ;                                                  [local-env (extend-env items-env env)])
    ;                                             (last
    ;                                              (map (lambda (e) (interp e local-env))
    ;                                                   body)))]
                                                                                                  
    ;; 调用
    [(list op-exp arg-exps ...) (let ([op-value (interp op-exp env)]
                                      [arg-values (map (lambda (arg-exp) (interp arg-exp env)) arg-exps)])
                                  (match op-value
                                    [(Closure params body closure-env)
                                     (let ([local-env (extend-env (make-env params arg-values) closure-env)])
                                       (last (map
                                              (lambda (e) (interp e local-env))
                                              body)))]
                                    [else (apply op-value arg-values)]))]))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; 解释器CPS

(define (interp/CPS exp env k)
  (match exp
    [(? self-valued?) (k exp)]
    [(? variable?)
     (let ([value (lookup-env exp env)])
       (if (not-found? value)
           (error "not found variable:" exp)
           (k value)))]

    ;; lambda表达式
    [(list 'lambda (list params ...) body ...)
     (schedule
      (lambda ()
        (k (Closure params body env)))
      (make-task-label 'interp/CPS/lambda env)
      50
      (lambda () exp))]

    ;; if表达式
    [(list 'if pred true-branch false-branch)
     (schedule
      (lambda ()
        (interp/CPS pred env
                    (lambda (pred-value)
                      (if pred-value
                          (interp/CPS true-branch env k)
                          (interp/CPS false-branch env k)))))
      (make-task-label 'interp/CPS/if env)
      100
      (lambda () exp))]
    
    ;; let表达式-语法糖
    ;    [(list 'let (list items ...) body ...) (let* ([params (map car items)]
    ;                                                  [args (map cadr items)]
    ;                                                  [let-sugar (append
    ;                                                              (list (append (list 'lambda params) body))
    ;                                                              args)])
    ;                                             (interp/CPS let-sugar env k))]

    ;; let表达式-独立特性
    [(list 'let (list items ...) body ...)
     (schedule
      (lambda ()
        (map/CPS
         (lambda (item k)
           (k (cadr item)))
         items
         (lambda (value-exps)
           (map/CPS
            (lambda (value-exp k)
              (interp/CPS value-exp env k))
            value-exps
            (lambda (values)
              (map/CPS
               (lambda (item k)
                 (k (car item)))
               items
               (lambda (keys)
                 (let* ([items-env (make-env keys values)]
                        [local-env (extend-env items-env env)])
                   (map/CPS
                    (lambda (e k)
                      (interp/CPS e local-env k))
                    body
                    (lambda (body-values)
                      (k (last body-values))))))))))))
      (make-task-label 'interp/CPS/let env)
      200
      (lambda () exp))]
                                                                                                  
    ;; 调用
    [(list op-exp arg-exps ...)
     (schedule
      (lambda ()
        (interp/CPS op-exp env
                    (lambda (op-value)
                      (map/CPS
                       (lambda (arg-exp k)
                         (interp/CPS arg-exp env k))
                       arg-exps
                       (lambda (arg-values)
                         (match op-value
                           [(Closure params body closure-env)
                            (let ([local-env
                                   (extend-env
                                    (make-env params arg-values)
                                    closure-env)])
                              (map/CPS
                               (lambda (e k)
                                 (interp/CPS e local-env k))
                               body
                               (lambda (body-values)
                                 (k (last body-values)))))]
                           [else (k (apply op-value arg-values))]))))))
      (make-task-label 'interp/CPS/call env)
      300
      (lambda () exp))]))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; 测试

(define (interp1)
  (define code '(((lambda (x)
                    (lambda (y)
                      (+ x y))) 23) 22)) ; => 45
  (interp code init-env))

(define (interp2)
  (define code '((((lambda (x)
                     (lambda (y)
                       (if (< x y)
                           (lambda (a) (* 10 a))
                           (lambda (a) (+ 10 a))))) 2) 100) 6)) ; => 60
  (interp code init-env))

(define (interp3)
  (define code '(let ([x 3])
                  (let ([y 2])
                    (let ([z 100])
                      (+ z (+ x y)))))) ; => 105
  (interp code init-env))

(define (interp4)
  (define code '(let ([x 3])
                  (let ([f (lambda () x)])
                    (let ([x 1000])
                      (f))))) ; => 3
  (interp code init-env))

(define (interp5)
  (define code '(((lambda (x y)
                    (if (< x y)
                        (lambda (a b) (+ a b))
                        (lambda (c d) (* c d)))) 10 20) 15 15)) ; => 30
  (interp code init-env))

(define (interp6)
  (define code '(let ([x 2]
                      [y 3]
                      [z 100])
                  (let ([x (+ x x)] ; 4
                        [y (* y y)]); 9
                    (+ x x)
                    (+ y y)
                    (+ z x y)))) ; => 113
  (interp code init-env))

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
  (interp code init-env))

(define (interp8)
  (define code '(let ([x 2]
                      [y 3]
                      [z 100])
                  (let ([x (+ x x)] ; 4
                        [y (* y y)]); 9
                    (println "hello")
                    (println "world")
                    (+ z x y)))) ; => 113
  (interp code init-env))

(define (interp9)
  (define code '(let ([x 2])
                  (let ([f (lambda () x)])
                    (let ([x 100])
                      (f))))) ; => 2
  (interp code init-env))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; 测试CPS

(define (interp1/CPS)
  (define code '(((lambda (x)
                    (lambda (y)
                      (+ x y))) 23) 22)) ; => 45
  (interp/CPS code init-env println))

(define (interp2/CPS)
  (define code '((((lambda (x)
                     (lambda (y)
                       (if (< x y)
                           (lambda (a) (* 10 a))
                           (lambda (a) (+ 10 a))))) 2) 100) 6)) ; => 60
  (interp/CPS code init-env println))

(define (interp3/CPS)
  (define code '(let ([x 3])
                  (let ([y 2])
                    (let ([z 100])
                      (+ z (+ x y)))))) ; => 105
  (interp/CPS code init-env println))

(define (interp4/CPS)
  (define code '(let ([x 3])
                  (let ([f (lambda () x)])
                    (let ([x 1000])
                      (f))))) ; => 3
  (interp/CPS code init-env println))

(define (interp5/CPS)
  (define code '(((lambda (x y)
                    (if (< x y)
                        (lambda (a b) (+ a b))
                        (lambda (c d) (* c d)))) 10 20) 15 15)) ; => 30
  (interp/CPS code init-env println))

(define (interp6/CPS)
  (define code '(let ([x 2]
                      [y 3]
                      [z 100])
                  (let ([x (+ x x)] ; 4
                        [y (* y y)]); 9
                    (+ x x)
                    (+ y y)
                    (+ z x y)))) ; => 113
  (interp/CPS code init-env println))

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
  (interp/CPS code init-env println))

(define (interp8/CPS)
  (define code '(let ([x 2]
                      [y 3]
                      [z 100])
                  (let ([x (+ x x)] ; 4
                        [y (* y y)]); 9
                    (println "hello")
                    (println "world")
                    (+ z x y)))) ; => 113
  (interp/CPS code init-env println))

(define (interp9/CPS)
  (define code '(let ([x 2])
                  (let ([f (lambda () x)])
                    (let ([x 100])
                      (f))))) ; => 2
  (interp/CPS code init-env println))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;s

; 测试并发

(define (make-task-label running-f-name env)
  (let ([task-id (symbol->string (lookup-env 'task-id env))]
        [task-name (symbol->string running-f-name)])
    (string-append task-id " " task-name)))
  
(define (interp/CPS/schedule/priority)
  (use-concurrent-priority)
  
  (define code1 '((((lambda (x)
                      (lambda (y)
                        (if (< x y)
                            (lambda (a) (* 10 a))
                            (lambda (a) (+ 10 a))))) 2) 100) 6)) ; => 60
  (define init-env1
    (add-env 'task-id 'task1
             init-env))
  (interp/CPS code1 init-env1 println)

  (define code2 '(let ([x 2]
                       [y 3]
                       [z 100])
                   (let ([x (+ x x)] ; 4
                         [y (* y y)]); 9
                     (println "hello")
                     (println "world")
                     (+ z x y)))) ; => 113
  (define init-env2
    (add-env 'task-id 'task2
             init-env))
  (interp/CPS code2 init-env2 println)

  (task-loop))
