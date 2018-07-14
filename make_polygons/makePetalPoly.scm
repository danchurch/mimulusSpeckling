(define(makePetalPoly filename)
    (let* (
            ;; load files, set vars
            (image (car (gimp-file-load 
                                0 
                                filename 
                                filename
                        ) 
                    ) 
            )
            (drawable (car (gimp-image-get-active-layer image)))
          )
            ;; do stuff
            ;;1 select black/solid regions:
            (gimp-image-select-color 
                image
                CHANNEL-OP-REPLACE
                drawable
                '(0 0 0) ;; black
            )
            ;;2 Convert selection to path
            (plug-in-sel2path
                RUN-NONINTERACTIVE
                image
                drawable
            ) 
            ;;3 save path to file
        (gimp-vectors-export-to-file
            image
            ;"/Users/danthomas/Documents/speckling/make_polygons/spots_script_test.svg"
            "/home/daniel/mimulusSpeckling/make_polygons/spots_script_test.svg" 
            0 ;; all vectors
        )
        (gimp-image-delete image)
        ;(set! filelist (cdr filelist))
    )
)
