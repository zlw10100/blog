#lang racket

;; 构造基础的并发系统，提供事件循环、任务队列、调度方案

(provide schedule)
(provide task-loop)
(provide get-now-time)
(provide queue)
(provide use-concurrent-loop)
(provide use-concurrent-priority)
(provide use-concurrent-count)
(provide use-concurrent-time)
(provide init-global-time)
(provide init-time-piece)
(provide log-opened)
(provide Task)
(provide Task-f)
(provide Task-label)
(provide Task-priority)
(provide Task-description-f)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; 循环调度方案

(define (schedule/loop task)
  (display-add-queue task)
  (add-queue! task))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; 优先级调度方案

(define (schedule/priority task)
  (display-add-queue task)
  (add-queue-by-priority! task >))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; 执行次数调度方案

(define count-config (list
                      `(sumC . ,(mcons 1 5))
                      `(prodC . ,(mcons 1 2))
                      ))

(define (select-count label)
  (let ([result (assq label count-config)])
    (if result
        (cdr result)
        (error "not found count config for:" label))))

(define (check-continue/count task)
  (let ([label (Task-label task)])
    (let ([count (select-count label)])
      (let ([current (mcar count)]
            [max (mcdr count)])
        (if (>= current max)
            (begin
              (set-mcar! count 1)
              #f)
            (begin
              (set-mcar! count (+ current 1))
              #t))))))

(define (schedule/count task)
  (if (check-continue/count task)
      (begin
        (display-execute task)
        ((Task-f task)))
      (begin
        (display-add-queue task)
        (add-queue! task))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; 执行时间调度方案

(define get-now-time current-milliseconds)

(define global-time (get-now-time))

(define time-piece 100) ; milliseconds

(define (init-time-piece ms)
  (set! time-piece ms))

(define (sleep-milliseconds s)
  (sleep (/ s 1000)))

(define (init-global-time)
  (set! global-time (get-now-time)))

(define (check-continue/time task)
  (let ([now (get-now-time)]
        [timeout (+ global-time time-piece)])
    (if (< now timeout)
        #t
        (begin
          (set! global-time now)
          #f))))

(define (schedule/time task)
  (if (check-continue/time task)
      (begin
        (display-execute task)
        ((Task-f task)))
      (begin
        (display-add-queue task)
        (add-queue! task))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; 任务队列和任务循环

(define queue '())

(struct Task (f label priority description-f))

(define log-opened #t)

(define (display-add-queue task)
  (if log-opened
      (printf "[~a add queue] ~a~n" (Task-label task) ((Task-description-f task)))
      (void)))

(define (display-execute task)
  (if log-opened
      (printf "[~a execute] ~a~n" (Task-label task) ((Task-description-f task)))
      (void)))

(define (add-queue! task)
  (set! queue
        (append queue (list task))))

(define (add-queue-by-priority! task compare)
  (define (recursive-add task queue)
    (if (empty? queue)
        `(,task)
        (let* ([priority (Task-priority task)]
               [current-task (car queue)]
               [current-priority (Task-priority current-task)]
               [rest-queue (cdr queue)])
          (if (compare priority current-priority)
              (cons task queue)
              (cons current-task (recursive-add task rest-queue))))))
  (set! queue (recursive-add task queue)))

(define (shift-queue!)
  (set! queue (cdr queue)))

(define (task-loop)
  (if (empty? queue)
      (printf "[task loop] all tasks done!~n")
      (let ([current-task (car queue)])
        (shift-queue!) ; shfit-queue!要在task执行之前触发，否则会移除不是期望的task
        (display-execute current-task)
        ((Task-f current-task))
        (task-loop))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; 切换调度方案

(define concurrent-plan schedule/loop)

(define (use-concurrent-loop)
  (set! concurrent-plan schedule/loop))

(define (use-concurrent-priority)
  (set! concurrent-plan schedule/priority))

(define (use-concurrent-count)
  (set! concurrent-plan schedule/count))

(define (use-concurrent-time)
  (set! concurrent-plan schedule/time))

(define (schedule f label priority description-f)
  (concurrent-plan (Task f label priority description-f)))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; CPS业务函数

(define (sumC n k)
  (schedule
   (lambda ()
     (sleep-milliseconds 20)
     (if (= n 0)
         (k 0)
         (sumC (- n 1)
               (lambda (result) (k (+ n result))))))
   'sumC
   100
   (lambda () (string-append "sumC:" (number->string n)))))

(define (prodC n k)
  (schedule
   (lambda ()
     (sleep-milliseconds 33)
     (if (= n 1)
         (k 1)
         (prodC (- n 1)
                (lambda (result) (k (* n result))))))
   'prodC
   200
   (lambda () (string-append "prodC:" (number->string n)))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; 测试

(define (run/schedule/loop)
  (use-concurrent-loop)
  (sumC 10 println)
  (prodC 10 println)
  (task-loop))

(define (run/schedule/priority)
  (use-concurrent-priority)
  (sumC 10 println)
  (prodC 10 println)
  (task-loop))

(define (run/schedule/count)
  (use-concurrent-count)
  (sumC 10 println)
  (prodC 10 println)
  (task-loop))

(define (run/schedule/time)
  (use-concurrent-time)
  (init-global-time)
  (sumC 10 println)
  (prodC 10 println)
  (task-loop))
