# QR → AR Experience (No App Required)

Scan a QR code → phone browser opens instantly → 3D augmented reality plays.

**Zero app installs. Works on iPhone Safari + Android Chrome.**

---

## 🗂 Project Structure

```
qr-ar-experience/
├── index.html              ← AR web experience (GitHub Pages site)
├── generate_qr.py          ← Python script to produce the QR PNG
├── requirements.txt        ← Python deps
├── media/                  ← Drop your videos, images, 3D models here
└── .github/
    └── workflows/
        └── deploy.yml      ← Auto-deploys to GitHub Pages on push
```

---

## 🚀 Quick Start

### Step 1 — Push to GitHub

```bash
cd qr-ar-experience
git init
git add .
git commit -m "init: AR experience"

# Create a new repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/qr-ar-experience.git
git push -u origin main
```

### Step 2 — Enable GitHub Pages

1. Go to your repo on GitHub
2. **Settings → Pages**
3. Under *Build and deployment*, choose:
   - Source: **GitHub Actions**
4. Push triggers the workflow → your site is live at:
   ```
   https://YOUR_USERNAME.github.io/qr-ar-experience/
   ```

### Step 3 — Generate the QR Code

```bash
# Install Python deps
pip install -r requirements.txt

# Generate QR pointing to your live URL
python generate_qr.py --url https://YOUR_USERNAME.github.io/qr-ar-experience/
```

This outputs `qr_code.png` — print it, share it, done!

---

## 📱 How It Works

| Step | What Happens |
|------|-------------|
| Phone scans QR | Camera app opens URL in browser |
| Browser loads page | Detects mobile, shows camera prompt |
| User taps "Allow" | Camera opens, AR scene launches |
| A-Frame renders 3D | Animated orbs float in your real world |
| No app install | 100% browser-native (WebXR + getUserMedia) |

---

## 🔧 Customization

### Change the 3D content
Edit `index.html`, find `<a-entity id="orb-group">` and replace/add A-Frame primitives:
- `<a-box>`, `<a-sphere>`, `<a-cylinder>` for basic shapes
- `<a-gltf-model src="media/your-model.glb">` for a 3D model
- `<a-video src="media/video.mp4">` for a floating video plane

### Change QR colors
Edit `generate_qr.py`:
```python
QR_FILL_COLOR = "#1a0533"   # dark module color
QR_BACK_COLOR = "#ffffff"   # background
```

### Add a logo to QR center
```bash
python generate_qr.py --logo media/logo.png
```

---

## 📋 Requirements

| Tool | Version |
|------|---------|
| Python | 3.9+ |
| qrcode | 7.x |
| Pillow | 10.x |

Device support:
- ✅ Android Chrome 79+
- ✅ iPhone Safari 15+ (WebXR flag on, or camera fallback)
- ✅ iPad Safari

---

## 📄 License

MIT — free to use and modify.
