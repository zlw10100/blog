#lang racket

;; 使用call/cc实现多任务并发调度，业务函数direct style

(require racket/control)

(define queue '())

(define (enqueue! t)
  (set! queue (append queue (list t))))

(define (dequeue!)
  (let ([t (car queue)])
    (set! queue (cdr queue))
    t))

(define loop-cont #f)

(define (sched)
  (call/cc
   (lambda (k)
     (enqueue! k)
     (loop-cont))))

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
    [else (call/cc
           (lambda (k)
             (set! loop-cont k)
             ((dequeue!))))
          (loop)]))

(add-task (lambda () (printf "sum(10) = ~a~n" (sum 10 'task1))))
(add-task (lambda () (printf "sum(10) = ~a~n" (sum 10 'task2))))

(loop)

