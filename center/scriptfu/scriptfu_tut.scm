;; try out a scriptfu tutorial. I think that the scriptfu language is the 
;; more current way of scripting for gimp.

;; our scripts directory is at:

;; /Users/danthomas/Library/Application Support/GIMP/2.8/scripts

;; following the example at <https://docs.gimp.org/en/gimp-using-script-fu-tutorial-first-script.html>


  (script-fu-register
            "script-fu-text-box"                        ;func name
            "Text Box"                                  ;menu label
            "Creates a simple text box, sized to fit\
              around the user's choice of text,\
              font, font size, and color."              ;description
            "Michael Terry"                             ;author
            "copyright 1997, Michael Terry;\
              2009, the GIMP Documentation Team"        ;copyright notice
            "October 27, 1997"                          ;date created
            ""                     ;image type that the script works on
            SF-STRING      "Text"          "Text Box"   ;a string variable
            SF-FONT        "Font"          "Charter"    ;a font variable
            SF-ADJUSTMENT  "Font size"     '(50 1 1000 1 10 0 1)
                                                        ;a spin-button
            SF-COLOR       "Color"         '(0 0 0)     ;color variable
            SF-ADJUSTMENT  "Buffer amount" '(35 0 100 1 10 1 0)
                                                        ;a slider
  )

  (script-fu-menu-register "script-fu-text-box" "<Image>/File/Create/Text")
  (define (script-fu-text-box inText inFont inFontSize inTextColor inBufferAmount)
    (let*
      (
        ; define our local variables
        ; create a new image:
        (theImageWidth  10)
        (theImageHeight 10)
        (theImage)
        (theImage
                  (car
                      (gimp-image-new
                        theImageWidth
                        theImageHeight
                        RGB
                      )
                  )
        )
        (theText)             ;a declaration for the text
;        (theBuffer)           ;create a new layer for the image
        (theLayer
                  (car
                      (gimp-layer-new
                        theImage
                        theImageWidth
                        theImageHeight
                        RGB-IMAGE
                        "layer 1"
                        100
                        NORMAL
                      )
                  )
        )
      ) ;end of our local variables
      (gimp-image-add-layer theImage theLayer 0)

;; just to check:
(gimp-display-new theImage)

;      (gimp-context-set-background '(255 255 255) )
;      (gimp-context-set-foreground inTextColor)
;      (gimp-drawable-fill theLayer BACKGROUND-FILL)
;      (set! theText
;                    (car
;                          (gimp-text-fontname
;                          theImage theLayer
;                          0 0
;                          inText
;                          0
;                          TRUE
;                          inFontSize PIXELS
;                          "Sans")
;                      )
;        )
;      (set! theImageWidth   (car (gimp-drawable-width  theText) ) )
;      (set! theImageHeight  (car (gimp-drawable-height theText) ) )
;      (set! theBuffer (* theImageHeight (/ inBufferAmount 100) ) )
;      (set! theImageHeight (+ theImageHeight theBuffer theBuffer) )
;      (set! theImageWidth  (+ theImageWidth  theBuffer theBuffer) )
;      (gimp-image-resize theImage theImageWidth theImageHeight 0 0)
;      (gimp-layer-resize theLayer theImageWidth theImageHeight 0 0)
;      (gimp-layer-set-offsets theText theBuffer theBuffer)
;      (gimp-display-new theImage)
;      (list theImage theLayer theText)
;    )
;  )
      
