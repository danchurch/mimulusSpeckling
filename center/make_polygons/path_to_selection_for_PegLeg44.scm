;script as described by PegLeg44 here: http://gimpchat.com/viewtopic.php?f=9&t=14046
;-----------------------------------------------------------------------------------
;I use the pen tool to select areas of the canvas (usually closed paths).
;1. I turn the path to a [Selection] [From Path].
;2. I create a new white layer.
;3. And fill the selection with black [Fill with Foreground Color].
;4. And then un-select [Select] [None].
;5. Then I run the [Colors] [Threshold] on the layer (with the standard 127 and 255 setting).
;6. And run [Layers] [Transparency] [Color to Alpha] on it.
;7. Then click the button [Lock Alpha Channel] at the top of the layers dockable dialog.
;8. Change the layer mode to [Darken Only]
;9. And finally use [Colors] [Invert] on it to make the black white.

(define (script-fu-path-to-selection-for-pegleg44 image layer 
         )
	
		(let* 
		   (
		   (width (car (gimp-image-width image)))
		   (height (car (gimp-image-height image)))
		   (active-vectors 0)
		   (new-layer 0)
		   )
			;(gimp-image-undo-disable image); DN = NO UNDO
			(gimp-context-push)
			(gimp-image-undo-group-start image)                   ;undo-group in one step
			
			
			;1. I turn the path to a [Selection] [From Path].
			(set! active-vectors (car (gimp-image-get-active-vectors image)))
			(gimp-image-select-item image CHANNEL-OP-REPLACE active-vectors)
			
			;2. I create a new white layer.
			(set! new-layer (car (gimp-layer-new image width height
	                           RGBA-IMAGE "new white" 100 NORMAL-MODE)))
			(gimp-drawable-fill new-layer WHITE-FILL)         ;fills background with white
			(gimp-image-insert-layer image new-layer 0 0) ;parent 0, insert layer on top position(0)				   
	
			;3. And fill the selection with black [Fill with Foreground Color].
			(gimp-edit-fill new-layer FOREGROUND-FILL)
			
			;4. And then un-select [Select] [None].
			(gimp-selection-none image)
			
			;5. Then I run the [Colors] [Threshold] on the layer (with the standard 127 and 255 setting).
			(gimp-threshold new-layer 127 255)
			
			;6. And run [Layers] [Transparency] [Color to Alpha] on it.
			(plug-in-colortoalpha 1 image new-layer '(255 255 255))
			
			;7. Then click the button [Lock Alpha Channel] at the top of the layers dockable dialog.
			(gimp-layer-set-lock-alpha new-layer TRUE)
			
			;8. Change the layer mode to [Darken Only]
			(gimp-layer-set-mode new-layer DARKEN-ONLY-MODE)
			
			;9. And finally use [Colors] [Invert] on it to make the black white.
			(gimp-invert new-layer)
		   ;(gimp-image-undo-enable image) ;DN = NO UNDO
			(gimp-image-undo-group-end image)                     ;undo group in one step
			(gimp-context-pop)
			(gimp-displays-flush)
	    )
	
	
    
) ;end of define
(script-fu-register
  "script-fu-path-to-selection-for-pegleg44"         ;function name
  "<Image>/Script-Fu/path-to-selection-for-PegLeg44 ..."    ;menu register
  "Steps described by PegLeg44 "       ;description
  "Tin Tran"                          ;author name
  "copyright info and description"         ;copyright info or description
  "2016"                          ;date
  "RGB*, GRAY*"                        ;mode
  SF-IMAGE      "Image" 0                   
  SF-DRAWABLE   "Layer" 0
  ;SF-STRING     "Text" "Gimp Chat"
)
