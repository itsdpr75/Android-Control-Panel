const { exec } = require('child_process');
const sqlite3 = require('sqlite3').verbose();

document.addEventListener('DOMContentLoaded', () => {
    const db = new sqlite3.Database('database.sqlite', (err) => {
        if (err) {
            console.error('Error opening database', err);
        } else {
            loadApps();  // Carga las apps
        }
    });

    function loadApps() {
        db.all("SELECT * FROM apps", [], (err, rows) => {
            if (err) {
                console.error('Error querying database', err);
                return;
            }
            const appGrid = document.getElementById('app-grid');
            rows.forEach(app => {
                const appIcon = createAppIcon(app.name, app.image_path, app.exec_path);
                appGrid.appendChild(appIcon);  // Añade el ícono al grid
            });
        });
    }

    function createAppIcon(name, imagePath, execPath) {
        const appIcon = document.createElement('div');
        appIcon.className = 'app-icon';

        const img = document.createElement('img');
        img.src = imagePath;  // Asegúrate de que la imagen se carga desde aquí
        img.alt = name;

        const span = document.createElement('span');
        span.textContent = name;

        appIcon.appendChild(img);
        appIcon.appendChild(span);

        appIcon.addEventListener('click', () => {
            executeProgram(execPath);
        });

        return appIcon;
    }
});
