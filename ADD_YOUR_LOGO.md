# How to Add Your Chengeta Logo

## 📁 Where to Place Your Logo

Copy your logo file to this folder:
```
C:\Users\Audry\finances-_tracker_tool\static\img\
```

## 📝 File Naming

Rename your logo file to one of these names:

### **Option 1: PNG (Recommended)**
```
logo.png
```
- Best for: Photos, complex graphics
- Supports: Transparency
- File size: Can be larger

### **Option 2: SVG (Best for scaling)**
```
logo.svg
```
- Best for: Vector graphics, icons
- Supports: Perfect scaling at any size
- File size: Smallest

### **Option 3: JPG**
```
logo.jpg
```
- Best for: Simple logos without transparency
- File size: Smaller than PNG

---

## 🎨 Logo Specifications

### **Dimensions**

#### Navigation Logo (Top bar)
- **Height**: 40px
- **Width**: Auto (maintains aspect ratio)
- **Max Width**: 40px
- **Format**: Square or horizontal

#### Auth Pages Logo (Login/Register)
- **Height**: 80px
- **Width**: Auto
- **Max Width**: 200px
- **Format**: Any shape

#### Footer Logo
- **Height**: 35px
- **Width**: Auto
- **Max Width**: 35px

### **Recommended Sizes**
- **Original**: 512×512px or larger
- **Navigation**: Will auto-resize to 40px height
- **Auth**: Will auto-resize to 80px height

---

## 🎯 Quick Steps

### **Step 1: Prepare Your Logo**
1. Export/save your logo
2. Recommended size: 512×512px
3. Format: PNG with transparent background (best)
4. OR: SVG for perfect scaling

### **Step 2: Name It**
```
logo.png
```

### **Step 3: Copy to Folder**
```
C:\Users\Audry\finances-_tracker_tool\static\img\logo.png
```

### **Step 4: Restart Server**
```bash
# Stop current server (Ctrl+C)
# Then restart:
python app.py
```

### **Step 5: Refresh Browser**
```
http://localhost:5000
```

**Your logo will appear automatically!**

---

## 📍 Where Your Logo Appears

### ✅ Navigation Bar (All Pages)
- Dashboard
- Transactions
- Budgets
- Reports
- Settings

### ✅ Landing Page
- Top navigation
- Footer

### ✅ Auth Pages
- Login page (large)
- Registration page (large)

---

## 💡 Logo Design Tips

### **For Best Results**

1. **Transparent Background**
   - Use PNG with alpha channel
   - OR use SVG

2. **Square or Horizontal**
   - Square: 512×512px
   - Horizontal: 512×256px

3. **Simple & Clear**
   - Recognizable at small sizes
   - Clear at 40px height
   - Good contrast

4. **Color Harmony**
   - Match Chengeta colors:
     - Green: #10b981
     - Cyan: #0891b2
   - OR: Full color logo

---

## 🔄 If Logo Doesn't Show

### **Troubleshooting**

1. **Check file name**
   - Must be exactly: `logo.png` (or .svg/.jpg)
   - Case-sensitive
   - No spaces

2. **Check file location**
   ```
   static/img/logo.png  ✓ Correct
   static/logo.png      ✗ Wrong
   img/logo.png         ✗ Wrong
   ```

3. **Restart server**
   - Stop with Ctrl+C
   - Run `python app.py` again

4. **Clear browser cache**
   - Hard refresh: Ctrl+Shift+R
   - Or: Ctrl+F5

5. **Check file permissions**
   - Make sure file is readable
   - Not corrupted

---

## ⚠️ Important Note

**Money bag emoji has been removed!** 

Your logo will be the only branding element. Make sure to add your logo file to avoid missing images.

---

## 📂 Current Status

**Logo Directory Created**: ✅
```
C:\Users\Audry\finances-_tracker_tool\static\img\
```

**Templates Updated**: ✅
- ✅ base.html (navigation)
- ✅ landing.html (header & footer)
- ✅ login.html
- ✅ register.html

**CSS Styles Added**: ✅
- ✅ Navigation logo (40px)
- ✅ Auth logo (80px)
- ✅ Footer logo (35px)

**Code Ready**: ✅
- ✅ Auto-detection
- ✅ Fallback emoji
- ✅ Responsive sizing

---

## 🚀 Next Steps

1. **Find your logo file**
2. **Rename to `logo.png`**
3. **Copy to `static/img/`**
4. **Restart server**
5. **Refresh browser**
6. **Enjoy your branded app!**

---

**Your logo will appear throughout Chengeta automatically!** 🎨✨

Need help? The app works perfectly with the emoji fallback until you add your logo!

