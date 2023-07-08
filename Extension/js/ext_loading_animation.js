

    // Function to start the animation
    function startAnimation() {
        document.getElementById("result-container").style.display = "none";
        document.getElementById("animationWindow").style.display = "block";
        if (animationInstance) {
            playAnimation(); // If initialized, play the animation
            return;
        }
        var animationWindow = document.querySelector("#animationWindow");
        var animData = {
        wrapper: animationWindow,
        animType: "svg",
        loop: true,
        prerender: true,
        autoplay: true,
        path: "https://s3-us-west-2.amazonaws.com/s.cdpn.io/35984/play_fill_loader.json",
        rendererSettings: {
            // Renderer settings here
            //context: canvasContext, // the canvas context
            scaleMode: "noScale",
            clearCanvas: false,
            progressiveLoad: false, // Boolean, only svg renderer, loads dom elements when needed. Might speed up initialization for large number of elements.
            hideOnTransparent: true, //Boolean, only svg renderer, hides elements when opacity reaches 0 (defaults to true)
        },
        };
    
        var anim = bodymovin.loadAnimation(animData);
        anim.addEventListener("DOMLoaded", onDOMLoaded);
        anim.setSpeed(1);
    
        function onDOMLoaded(e) {
        anim.addEventListener("complete", function () {
            // Animation complete event listener
        });
        }
        function playAnimation() {
        if (animationInstance) {
            animationInstance.play();
        }
        }
        animationInstance = anim;
    }
