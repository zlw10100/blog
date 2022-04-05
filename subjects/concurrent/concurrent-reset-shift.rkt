#lang racket

;; 使用reset/shift实现并发调度，业务函数direct style

(require racket/control)

(define queue '())

(define (enqueue! t)
  (set! queue (append queue (list t))))

(define (dequeue!)
  (let ([t (car queue)])
    (set! queue (cdr queue))
    t))

(define (sched)
  (shift k (enqueue! k)))

(define (add-task t)
  (enqueue! t))

(define (sum n title)
  (sched)
  (cond
    [(zero? n) 0]
    [else
     (printf "[~a] sum: ~a~n" title n)
     (+ n (sum (sub1 n) title))]))

(define (loop)
  (cond
    [(empty? queue) (println "all tasks done!")]
    [else (reset ((dequeue!)))
          (loop)]))

(sum 10 'task1)
(sum 10 'task2)

(loop)
