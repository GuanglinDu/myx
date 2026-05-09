Build a Full-Stack Social Network with Django and Vue 3: From Idea to Launch | Part 1/16
https://www.youtube.com/watch?v=xOxN_7coIDw&list=PLpyspNLjzwBlobEvnZzyWP8I-ORQcq4IO&index=1

The folder structure:
           --xfrontend
  twitter--|
	       --xbackend


(1/4) Create a new Vue.js 3 project named xfrontend from scratch
=================================================================
(env314) PS D:\repo-tauri\twitter> npm init vite@latest
Need to install the following packages:
create-vite@8.2.0
Ok to proceed? (y) y

> npx
> create-vite

│
◇  Project name:
│  xfrontend
│
◇  Select a framework:
│  Vue
│
◇  Select a variant:
│  TypeScript
│
◇  Use rolldown-vite (Experimental)?:
│  No
│
◇  Install with npm and start now?
│  Yes
│
◇  Scaffolding project in D:\repo-tauri\twitter\xfrontend...
│
◇  Installing dependencies with npm...

added 48 packages, and audited 49 packages in 24s

6 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
│
◇  Starting dev server...

> xfrontend@0.0.0 dev
> vite

Port 5173 is in use, trying another one...

  VITE v7.3.1  ready in 507 ms

  ➜  Local:   http://localhost:5174/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help


(2/4) npm install (Seems unnecessary)
=====================================
Terminate batch job (Y/N)? Y
(env314) PS D:\repo-tauri\twitter> codium .
(env314) PS D:\repo-tauri\twitter> cd .\xfrontend\
(env314) PS D:\repo-tauri\twitter\xfrontend> codium .
(env314) PS D:\repo-tauri\twitter\xfrontend> npm install

up to date, audited 49 packages in 1s

6 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
(env314) PS D:\repo-tauri\twitter\xfrontend>


(3/4) Install vue-router, pinia, and axios
=========================================
(env314) PS D:\repo-tauri\twitter\xfrontend> npm install axios

added 23 packages, and audited 72 packages in 11s

12 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities


(3.1/4) Install vue-router & pinia
-----------------------------------
npm install vue-router pinia

(env312) PS D:\repo-tauri\twitter\xfrontend> npm install vue-router pinia

added 47 packages, and audited 119 packages in 11s

27 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities


(4/4) Install tailwindcss
===========================
Install Tailwind CSS with Vue 3 and Vite
https://v2.tailwindcss.com/docs/guides/vue-3-vite

npm install -D tailwindcss@latest postcss@latest autoprefixer@latest

(env312) PS D:\repo-tauri\twitter\xfrontend> npm install -D tailwindcss@latest postcss@latest autoprefixer@latest

added 11 packages, and audited 130 packages in 11s

32 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
(env312) PS D:\repo-tauri\twitter\xfrontend>


(4.1/4) Create your configuration files
-------------------------------------------
Next, generate your tailwind.config.js and postcss.config.js files:

npx tailwindcss init -p


(4.2/4) Problems caused by the latest version
----------------------------------------------
(env312) PS D:\repo-tauri\twitter\xfrontend> npx tailwindcss init -p
npm error could not determine executable to run
npm error A complete log of this run can be found in: C:\Users\Guanglin\AppData\Local\npm-cache\_logs\2026-02-04T12_34_27_872Z-debug-0.log


(4.2/4) Fix: Use a lower version
---------------------------------------------
npm uninstall tailwindcss postcss autoprefixer

Install a specific version: npm install 'package_name'@'package_version'

Use the following in package.json

    "autoprefixer": "^10.4.14",
    "postcss": "^8.4.21",
    "tailwindcss": "^3.3.1",
	
npm install, and then,

(env312) PS D:\repo-tauri\twitter\xfrontend> npx tailwindcss init -p

Created Tailwind CSS config file: tailwind.config.js
Created PostCSS config file: postcss.config.js
(env312) PS D:\repo-tauri\twitter\xfrontend>
