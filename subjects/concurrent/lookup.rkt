#lang racket

;; 为解释器环境提供pair搜索

(provide empty-table)
(provide add-table)
(provide lookup-table)

(provide empty-bst)
(provide add-bst)
(provide lookup-bst)

(provide not-found?)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; 内置"未找到"对象
(struct not-found ())


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; 线性查找表
(define empty-table '())

(define add-table
  (lambda (key value old-table)
    (cond
      [(empty? old-table) `(,(cons key value))]
      [else (cons
             (cons key value)
             old-table)])))

(define lookup-table
  (lambda (key table)
    (let ([result (assq key table)])
      (if result
          (cdr result)
          (not-found)))))


(define menu0
  (list (cons 'a 23)
        (cons 'b 66)
        (cons 'c 75)))

(define menu1 (add-table "pizza" 18
                         (add-table "cake" 46
                                    (add-table "pasta" 68
                                               (add-table "steak" 258
                                                          (add-table "salad" 45
                                                                     (add-table "beer" 35 empty-table)))))))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; 二叉搜索树
(struct node (k v left right))

(define empty-bst '())

(define add-bst
  (lambda (key value old-bst)
    (cond
      [(empty? old-bst) (node key value '() '())]
      [else (let ([root-value (node-v old-bst)])
              (cond
                [(<= value root-value) (node
                                        (node-k old-bst)
                                        (node-v old-bst)
                                        (add-bst key value (node-left old-bst))
                                        (node-right old-bst))]
                [else (node
                       (node-k old-bst)
                       (node-v old-bst)
                       (node-left old-bst)
                       (add-bst key value (node-right old-bst)))]))])))

(define lookup-bst
  (lambda (key bst)
    (if (empty? bst)
        (not-found)
        (let ([root-key (node-k bst)])
          (cond
            [(symbol<? key root-key) (lookup-bst key (node-left bst))]
            [(symbol=? key root-key) (node-v bst)]        
            [else (lookup-bst key (node-right bst))])))))
        

(define bst-items
  (lambda (bst)
    (cond
      [(empty? bst) '()]
      [else (append
             (bst-items (node-left bst))
             (list (cons (node-k bst) (node-v bst)))
             (bst-items (node-right bst)))])))

(define r0 (add-bst 'a 23 empty-bst))
(define r1 (add-bst 'b 1 r0))
(define r2 (add-bst 'c 100 r1))
(define r3 (add-bst 'd -1 r2))
(define r4 (add-bst 'e 211 r3))









     



