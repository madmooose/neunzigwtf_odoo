odoo.define("rocket.bubble_background", function () {
    "use strict";

    const canvas = document.getElementById("bubble-canvas");
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    let lastPlingTime = 0;

    const bubbles = [];
    const createBubble = (width, height) => ({
        x: Math.random() * width,
        y: height + Math.random() * 100,
        size: Math.random() * 30 + 15,
        speedX: Math.random() * 0.7 - 0.35,
        speedY: -Math.random() * 0.8 - 0.7,
        opacity: Math.random() * 0.7 + 0.3,
        state: "rising",
        stateTime: 0,
        droplets: [],
        isPlinging: false,
        plingSize: 0,
        plingOpacity: 0,
    });

    const playPling = () => {
        const now = Date.now();
        if (now - lastPlingTime < 100) return;
        lastPlingTime = now;

        try {
            const oscillator = audioContext.createOscillator();
            const gain = audioContext.createGain();
            oscillator.connect(gain);
            gain.connect(audioContext.destination);
            oscillator.type = "sine";
            oscillator.frequency.setValueAtTime(600, audioContext.currentTime);
            oscillator.frequency.exponentialRampToValueAtTime(
                200,
                audioContext.currentTime + 0.2
            );
            gain.gain.setValueAtTime(0.0001, audioContext.currentTime);
            gain.gain.exponentialRampToValueAtTime(
                0.1,
                audioContext.currentTime + 0.01
            );
            gain.gain.exponentialRampToValueAtTime(
                0.0001,
                audioContext.currentTime + 0.3
            );
            oscillator.start();
            oscillator.stop(audioContext.currentTime + 0.3);
        } catch (e) {
            console.error("Pling error:", e);
        }
    };

    const resize = () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    };
    resize();
    window.addEventListener("resize", resize);

    const count = Math.floor(window.innerWidth / 20);
    for (let i = 0; i < count; i++) {
        bubbles.push(createBubble(canvas.width, canvas.height));
    }

    let lastTime = 0;
    const animate = (time) => {
        const dt = time - lastTime;
        lastTime = time;

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "rgb(10, 10, 10)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        bubbles.forEach((bubble, i) => {
            // Rising
            if (bubble.state === "rising") {
                bubble.x += bubble.speedX;
                bubble.y += bubble.speedY;
                if (bubble.y <= bubble.size) {
                    bubble.state = "condensing";
                    bubble.stateTime = 0;
                    bubble.isPlinging = true;
                    bubble.plingSize = bubble.size * 1.5;
                    bubble.plingOpacity = 1;
                    bubble.y = bubble.size;
                    playPling();
                }
            }

            // Condensing
            if (bubble.state === "condensing") {
                bubble.stateTime += dt;
                bubble.size = Math.max(0, bubble.size - 0.002 * dt * bubble.size);
                bubble.opacity = Math.max(0, bubble.opacity - 0.001 * dt);
                if (bubble.size < 2 || bubble.opacity <= 0.05) {
                    bubble.state = "drop";
                    bubble.stateTime = 0;
                }
            }

            // Drop
            if (bubble.state === "drop") {
                if (bubble.droplets.length === 0) {
                    bubbles[i] = createBubble(canvas.width, canvas.height);
                }
            }

            // Draw
            if (bubble.state !== "drop" && bubble.size > 0) {
                ctx.beginPath();
                ctx.arc(bubble.x, bubble.y, bubble.size, 0, Math.PI * 2);
                const grad = ctx.createRadialGradient(
                    bubble.x,
                    bubble.y,
                    0,
                    bubble.x,
                    bubble.y,
                    bubble.size
                );
                grad.addColorStop(0, `rgba(170,255,0,${bubble.opacity})`);
                grad.addColorStop(0.7, `rgba(57,255,20,${bubble.opacity * 0.8})`);
                grad.addColorStop(1, `rgba(0,255,68,${bubble.opacity * 0.6})`);
                ctx.fillStyle = grad;
                ctx.fill();
            }

            if (bubble.isPlinging) {
                ctx.beginPath();
                ctx.arc(bubble.x, bubble.y, bubble.plingSize, 0, Math.PI * 2);
                ctx.strokeStyle = `rgba(170,255,0,${bubble.plingOpacity})`;
                ctx.lineWidth = 2;
                ctx.stroke();
                bubble.plingSize += 1;
                bubble.plingOpacity -= 0.05;
                if (bubble.plingOpacity <= 0) {
                    bubble.isPlinging = false;
                }
            }
        });

        requestAnimationFrame(animate);
    };

    document.addEventListener("click", () => {
        if (audioContext.state === "suspended") {
            audioContext.resume();
        }
    });

    animate(0);
});
