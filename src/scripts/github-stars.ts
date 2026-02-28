async function fetchStars() {
	const starElements = document.querySelectorAll('.github-stars');
	const repoData: { repo: string; starsCount: number }[] = [];
	let maxStars = 0;

	for (const el of starElements) {
		const repo = el.getAttribute('data-repo');
		if (!repo) continue;

		try {
			const res = await fetch(`https://api.github.com/repos/${repo}`);
			const data = await res.json();

			const starsCount = data.stargazers_count || 0;
			if (starsCount > maxStars) maxStars = starsCount;

			repoData.push({ repo, starsCount });

			const stars = new Intl.NumberFormat('en-US', {
				notation: "compact",
				compactDisplay: "short"
			}).format(starsCount);

			el.textContent = stars;
		} catch {
			el.textContent = "Error";
		}
	}

	if (maxStars > 0) {
		for (const { repo, starsCount } of repoData) {
			const container = document.querySelector<HTMLElement>(`[data-bar-repo="${repo}"]`);
			const fill = document.querySelector<HTMLElement>(`[data-bar-fill="${repo}"]`);
			if (container && fill) {
				container.style.display = 'block';
				const percentage = Math.max((starsCount / maxStars) * 100, 1);
				setTimeout(() => {
					fill.style.width = `${percentage}%`;
				}, 100);
			}
		}
	}
}

fetchStars();
