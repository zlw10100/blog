#lang racket

(define dont-cps-ls
  '(+ - * / = > < >= <=))

(define (dont-cps? fn)
  (member fn dont-cps-ls))

(define id (lambda (x) x))

(define (make-symbol base index)
  (string->symbol
   (string-append
    (symbol->string base)
    (number->string index))))

(define (make-gen base)
  (mcons base 0))

(define (gensym gen)
  (let ([index (mcdr gen)]
        [base (mcar gen)])
    (set! index (add1 index))
    (set-mcdr! gen index)
    (if (= index 0)
        base
        (make-symbol base index))))

(define (gensym-clear gen)
  (set-mcdr! gen -1))

(define genv (make-gen 'v))
(define genk (make-gen 'k))

(define tail-ctx (lambda (x) `(k ,x)))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (cpser-args args ctx)
  (if (empty? args)
      (ctx '())
      (cpser1 (car args) (lambda (x)
                           (cpser-args (cdr args) (lambda (v)
                                                    (ctx (cons x v))))))))

(define (cpser1 exp ctx)
  (match exp
    
    [(? symbol? exp)
     (ctx exp)
     ]
    
    [(? number? exp)
     (ctx exp)
     ]
   
    [`(lambda (,params ...) ,body)
     (ctx `(lambda (,@params k)
             ,(cpser1 body tail-ctx)))
     ]

    [`(if ,pred ,tb ,fb)
     (cpser1 pred (lambda (p)
                    `(if ,p
                         ,(cpser1 tb ctx)   ;; if这里有重复的上下文会编译重复的代码
                         ,(cpser1 fb ctx))))
     ]

    [`(let ((,name ,val)) ,body)
     (let ([sugar-call `((lambda (,name) ,body) ,val)])
       ; (printf "sugar call: ~a~n" sugar-call)
       (cpser1 sugar-call ctx))
     ]

    [`(define ,name ,val)
     `(define ,name ,(cpser1 val ctx))
     ]

    [`(,op ,args ...)
     (if (dont-cps? op)
         (cpser-args args (lambda (av)
                            (ctx `(,op ,@av))))
         (cpser1 op (lambda (x)
                      (cpser-args args (lambda (av)
                                         (if (eq? ctx tail-ctx)
                                             `(,x ,@av k)
                                             (let* ([v (gensym genv)])
                                               `(,x ,@av (lambda (,v) ,(ctx v))))))))))
     ]
    
    ;    [`(,op ,arg)
    ;     (if (dont-cps? op)
    ;         (cpser1 arg (lambda (y)
    ;                       (ctx `(,op ,y)))) 
    ;         (cpser1 op (lambda (x)
    ;                      (cpser1 arg (lambda (y)
    ;                                    (if (eq? ctx tail-ctx)
    ;                                        `(,x ,y k)
    ;                                        (let ([v (gensym genv)])
    ;                                          `(,x ,y (lambda (,v) ,(ctx v))))))))))
    ;     ]
     
    ;    [`(,binop ,e1 ,e2)
    ;     (cpser1 e1 (lambda (x)
    ;                  (cpser1 e2 (lambda (y)
    ;                               (let ([v (gensym genv)])
    ;                                 (ctx `(,binop ,x ,y)))))))
    ;     ]
       

    ))

(define (cpser exp)
  (gensym-clear genv)
  (gensym-clear genk)
  (cpser1 exp id))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(cpser '(lambda (x)
          (lambda (y)
            (y x))))
;(lambda (x k)
;  (k (lambda (y k)
;       (y x k))))



(cpser '(lambda (x)
            (+ (f 1)
               (g 2))))
;(lambda (x k)
;   (f 1 (lambda (v)
;          (g 2 (lambda (v1)
;                 (k (+ v v1)))))))



(cpser '(lambda (x) (f (g 2))))
;(lambda (x k)
;  (g 2 (lambda (v)
;         (f v k))))



(cpser '(if (f 1)
              (+ (g 2)
                 (h 3))
              (* (p 4)
                 (q 5))))
;(f 1 (lambda (v)
;       (if v
;           (g 2 (lambda (v1)
;                  (h 3 (lambda (v2)
;                         (+ v1 v2)))))
;           (p 4 (lambda (v3)
;                  (q 5 (lambda (v4)
;                         (* v3 v4))))))))



(define fact '(define fact
                (lambda (n)
                  (if (= n 0)
                      1
                      (* n (fact (- n 1)))))))
(cpser fact)
;(define fact
;  (lambda (n k)
;    (if (= n 0)
;        (k 1)
;        (fact (- n 1) (lambda (v)
;                        (k (* n v)))))))



(cpser '((lambda (f)
           (f 1))
         (lambda (g)
           (g 2))))
;((lambda (f k)
;   (f 1 k))
; (lambda (g k)
;   (g 2 k))
; (lambda (v) v))



(cpser '(let ([x 1])
            (f (g x)
               (h 3))))
;((lambda (x k)
;   (g x (lambda (v)
;          (h 3 (lambda (v1)
;                 (f v v1 k))))))
;  1
;  (lambda (v2) v2))


(cpser '(f 1 2 3 4))
;(f 1 2 3 4 (lambda (v) v))



(cpser '(f (g 0) (h 1) (p 2) (q 3)))
;(g 0 (lambda (v)
;       (h 1 (lambda (v1)
;              (p 2 (lambda (v2)
;                     (q 3 (lambda (v3)
;                            (f v v1 v2 v3 (lambda (v4) v4))))))))))


(cpser '(lambda (a b c)
            (f (h a)
               (p b)
               (q c))))
;(lambda (a b c k)
;    (h a (lambda (v)
;           (p b (lambda (v1)
;                  (q c (lambda (v2)
;                         (f v v1 v2 k))))))))



(cpser '((lambda (f)
             (f (g 0) (h 1) (n 2)))
           (lambda (a b c)
             (if (a (b c))
                 100
                 200))))
;((lambda (f k)
;   (g 0 (lambda (v) (h 1 (lambda (v1) (n 2 (lambda (v2) (f v v1 v2 k))))))))
; (lambda (a b c k)
;   (b c (lambda (v3) (a v3 (lambda (v4) (if v4 (k 100) (k 200)))))))
; (lambda (v5) v5))

