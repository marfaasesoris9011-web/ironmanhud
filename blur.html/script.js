const videoElement = document.getElementById("video");
const canvasElement = document.getElementById("canvas");
const canvasCtx = canvasElement.getContext("2d");
const statusText = document.getElementById("status");

const hands = new Hands({
    locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
    }
});

hands.setOptions({
    maxNumHands: 1,
    modelComplexity: 1,
    minDetectionConfidence: 0.7,
    minTrackingConfidence: 0.7
});

function fingerUp(tip, pip, landmarks) {
    return landmarks[tip].y < landmarks[pip].y;
}

function countFingers(hand) {

    let total = 0;

    if (hand[4].x < hand[3].x) total++;

    if (fingerUp(8, 6, hand)) total++;
    if (fingerUp(12, 10, hand)) total++;
    if (fingerUp(16, 14, hand)) total++;
    if (fingerUp(20, 18, hand)) total++;

    return total;
}

hands.onResults(results => {

    canvasElement.width = videoElement.videoWidth;
    canvasElement.height = videoElement.videoHeight;

    canvasCtx.save();

    canvasCtx.clearRect(
        0,
        0,
        canvasElement.width,
        canvasElement.height
    );

    if (results.multiHandLandmarks.length > 0) {

        const hand = results.multiHandLandmarks[0];

        drawConnectors(
            canvasCtx,
            hand,
            HAND_CONNECTIONS,
            {
                color: "#00ff66",
                lineWidth: 4
            }
        );

        drawLandmarks(
            canvasCtx,
            hand,
            {
                color: "#00ff66",
                radius: 5
            }
        );

        const fingers = countFingers(hand);

        if (fingers >= 5) {

            videoElement.classList.add("blur");
            statusText.innerHTML = " Blur Aktif";

        } else {

            videoElement.classList.remove("blur");
            statusText.innerHTML = " Kamera Normal";

        }

    } else {

        videoElement.classList.remove("blur");
        statusText.innerHTML = " Tampilkan Telapak Tangan";

    }

    canvasCtx.restore();

});

const camera = new Camera(videoElement, {

    onFrame: async () => {

        await hands.send({
            image: videoElement
        });

    },

    width: 1280,
    height: 720

});

camera.start();