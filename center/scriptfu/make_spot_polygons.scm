;; try to get a script running:
;; for the moment, this should just open a file and create 
;; a new one with the new user given name

(define (make-polygon inFile outFile) 

    ;; vars
    (let* ( 
            (image (car (gimp-file-load RUN-NONINTERACTIVE inFile) ) )
            (drawable (car (gimp-image-get-active-layer image)))
          )

    ;; expressions
    (gimp-file-save RUN-NONINTERACTIVE image drawable outFile outFile)

    (gimp-image-delete image)
    )
)


