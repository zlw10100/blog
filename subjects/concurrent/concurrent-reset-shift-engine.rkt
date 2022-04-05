#lang racket

;; 用reset/shift实现多任务并发，任务用engine提供时间片暂停，业务函数direct style

(require racket/control)
(require racket/engine)

(define queue '())

(define (enqueue! engine)
  (set! queue (append queue (list engine))))

(define (dequeue!)
  (let ([engine (car queue)])
    (set! queue (cdr queue))
    engine))

(define (sleep-milliseconds s)
  (sleep (/ s 1000)))

(define (sched)
  (shift k
         (enqueue!
          (make-engine (lambda (suspends) (k))))))

(define (make-engine f)
  (engine
   (lambda (suspends)
     (reset (f suspends)))))

(define (add-task f)
  (enqueue! (make-engine f)))

(define (sum n title)
  (sleep-milliseconds 2)
  
  (cond
    [(zero? n)
     (printf "[~a] sum done!~n" title)
     0]
    [(= n 3)
     (printf "[~a] sum ~a 主动切出~n" title n)
     (sched)
     (+ n (sum (sub1 n) title))] 
    [else
     (printf "[~a] sum: ~a~n" title n)
     (+ n (sum (sub1 n) title))]))

(define (prod n title)
  (sleep-milliseconds 5)
  
  (cond
    [(zero? n)
     (printf "[~a] prod done!~n" title)
     1]
    [else
     (printf "[~a] prod: ~a~n" title n)
     (* n (prod (sub1 n) title))]))


(define (loop)
  (if (empty? queue)
      (println "all tasks done!")
      (let* ([engine (dequeue!)]
             [result (engine-run 10 engine)]) ; engine时间片10ms
        (if (eq? result #f)
            (enqueue! engine)
            (void))
        (loop))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; 测试

(define (test)
  (add-task
   (lambda (suspends)
     (println (sum 10 'task1))))

  (add-task
   (lambda (suspends)
     (println (prod 10 'task2))))

  (loop))

