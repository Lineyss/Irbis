// Inject the file loading button at runtime
import * as SCENE from './scene.js';

let fileUrl = location.origin + '/media/' + document.getElementById("file").title
let workerUrl = location.origin + "/static/main/js/deploy/worker.js"

const worker = new Worker(workerUrl);
const setStatus = function(s) {
    console.log("Текущий статус: " + s)
};
let startTime, loadTimeShowing = false;
SCENE.addCameraCallback(function () {
    if (loadTimeShowing) {
        setStatus("");
    }
});

worker.onmessage = function(e) {
    setStatus("Building scene...");
    SCENE.loadMesh(e.data);
    fileSelector.disabled = false;

    const d = new Date();
    const now = d.getTime();
    const dt_sec = (now - startTime) / 1000.0;
    setStatus("Loaded in " + dt_sec.toPrecision(3) + " sec");
    loadTimeShowing = true;
}
const loadMeshFromString = function(s) {
    const d = new Date();
    startTime = d.getTime();
    setStatus("Parsing & triangulating...");
    worker.postMessage(s);
}

setStatus("загрузка файла по пути: " + fileUrl)

fetch(fileUrl)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    })
    .then(data => {
        loadMeshFromString(data);
        setStatus("File loaded from the link successfully!");
    })
    .catch(error => {
        setStatus("Error loading file from the link.");
        console.error('Error:', error);
    });

let exampleList;
function populateExamples(d) {
    var i = 1;
    exampleList = [];
    for (const ex of d) {
        var opt = document.createElement('option');
        opt.text = ex[0];
        opt.value = i;
        i += 1;
        exampleSelector.add(opt);
        exampleList.push(ex);
    }
}