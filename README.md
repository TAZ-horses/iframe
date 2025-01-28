
	<title>Tom Cox | Film Industry Horsemaster & Stunt Coordinator</title>
	<style>
		:root {
			--primary-dark: #2a423f;
			--accent-red: #ee0505;
			--secondary-dark: #2f3b2d;
			--light-bg: #f8f8f8;
			--ease: cubic-bezier(0.25, 0.46, 0.45, 0.94);
			--film-grain: url('https://i.imgur.com/3LnRxwD.png');
			--light-leak: linear-gradient(120deg, rgba(255, 200, 150, 0.3), rgba(255, 255, 255, 0) 70%);
		}

		@import url('https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;700&family=Instrument+Sans:wght@400;500&display=swap');

		body {
			font-family: 'Instrument Sans', system-ui, sans-serif;
			margin: 0;
			padding: 0;
			background: var(--light-bg);
			color: var(--primary-dark);
			overflow-x: hidden;
		}

		.container {
			width: 100%;
			height: 100vh;
			display: flex;
			justify-content: center;
			align-items: center;
			position: relative;
			overflow: hidden;
			background: #000;
		}

		.reel {
			width: 100%;
			height: 80%;
			display: flex;
			align-items: center;
			justify-content: space-between;
			animation: cinematic-slide 30s linear infinite;
			background-image: var(--film-grain);
			background-size: cover;
		}

		.reel-image {
			width: 100%;
			height: auto;
			max-height: 100%;
			object-fit: contain;
			filter: grayscale(80%) brightness(0.9) contrast(1.2);
			transition: filter 0.5s ease, transform 0.5s ease;
			cursor: pointer;
		}

		.reel-image:hover {
			filter: grayscale(0%) brightness(1.1) contrast(1.5);
		}

		.fullscreen {
			position: fixed;
			top: 0;
			left: 0;
			width: 100%;
			height: 100%;
			background: rgba(0, 0, 0, 0.9);
			display: flex;
			justify-content: center;
			align-items: center;
			z-index: 1000;
			visibility: hidden;
			opacity: 0;
			transition: visibility 0s, opacity 0.3s ease;
		}

		.fullscreen img {
			max-width: 90%;
			max-height: 90%;
			object-fit: contain;
		}

		.fullscreen.active {
			visibility: visible;
			opacity: 1;
		}

		@keyframes cinematic-slide {
			0% {
				transform: translateX(0);
			}
			100% {
				transform: translateX(-100%);
			}
		}
	</style>
</head>
<body>
	<div class="container">
		<div class="reel">
			<img class="reel-image" src="https://m.media-amazon.com/images/M/MV5BODYwZWI5NjItMDg3ZC00ZGY5LTk0ZDgtYTA2Y2VjYzVmNjM1XkEyXkFqcGc@._V1_QL75_UX820_.jpg" alt="Film Poster 1">
			<img class="reel-image" src="https://m.media-amazon.com/images/M/MV5BOTMyZWFjMGQtNWY4NC00MzFiLWE3MWMtYTI4N2I4NDYxMjM4XkEyXkFqcGc@._V1_.jpg" alt="Film Poster 2">
			<img class="reel-image" src="https://m.media-amazon.com/images/M/MV5BMzZhYzE1NzctZWY3MS00MjcwLWIyNjMtNjhkODY1Y2E5MDhhXkEyXkFqcGc@._V1_QL75_UX820_.jpg" alt="Film Poster 3">
			<img class="reel-image" src="https://m.media-amazon.com/images/M/MV5BMzExZDhhYjEtNGY4Ny00MWQwLTljNTQtMzBjYTk5NWM1OTEyXkEyXkFqcGc@._V1_QL75_UX820_.jpg" alt="Film Poster 4">
			<img class="reel-image" src="https://m.media-amazon.com/images/M/MV5BN2Y2ZWNlYjMtMjA1OC00OTY2LTg3MjItNTNjODEwYjg5ZGY3XkEyXkFqcGc@._V1_QL75_UX820_.jpg" alt="Film Poster 5">
			<img class="reel-image" src="https://m.media-amazon.com/images/M/MV5BNzM2MzI5OTMtNzZkMi00NzE2LWJjMWQtYTA4Y2UxNWMwZTg2XkEyXkFqcGc@._V1_QL75_UX820_.jpg" alt="Film Poster 6">
			<img class="reel-image" src="https://m.media-amazon.com/images/M/MV5BNThjNDJjNTQtZDhhMy00OWE5LTgzMDUtZDllMWRlZWY2NDk2XkEyXkFqcGc@._V1_QL75_UX820_.jpg" alt="Film Poster 7">
			<img class="reel-image" src="https://m.media-amazon.com/images/M/MV5BOWI3ODZjYjQtZWU2OS00MDVmLTljMTUtOTRiZTkzNjI0ZWY0XkEyXkFqcGc@._V1_QL75_UX820_.jpg" alt="Film Poster 8">
		</div>
	</div>
	<div class="fullscreen" id="fullscreen">
		<img src="" alt="Fullscreen Poster">
	</div>
	<script>
		const reelImages = document.querySelectorAll('.reel-image');
		const fullscreen = document.getElementById('fullscreen');
		const fullscreenImg = fullscreen.querySelector('img');

		reelImages.forEach(image => {
			image.addEventListener('click', () => {
				fullscreenImg.src = image.src;
				fullscreen.classList.add('active');
			});
		});

		fullscreen.addEventListener('click', () => {
			fullscreen.classList.remove('active');
		});
	</script>
</body>
</html>
