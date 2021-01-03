//Like or Unlike Toggle
window.addEventListener('DOMContentLoaded', function () {
	document.querySelectorAll('.like-toggle').forEach((toggle) => {
		toggle.addEventListener('click', function (event) {
			event.preventDefault();
			changePostLikeStatus(this.dataset.postId, this.dataset.likes, this);
		});
	});

	const changePostLikeStatus = (postId, likes, element) => {
		fetch(`/likes/${postId}`, {
			method: 'PUT',
			credentials: 'include', // For Cors
			credentials: 'same-origin',
			headers: {
				'X-CSRFToken': getCookie('csrftoken'),
			},
			body: JSON.stringify({
				like: likes,
			}),
		})
			.then(() => {
				if (element.classList.contains('btn-danger')) {
					element.classList.remove('btn-danger');
					element.classList.add('btn-primary');
					element.textContent = 'Like';
					element.dataset.likes = 'True';
				} else {
					element.classList.remove('btn-primary');
					element.classList.add('btn-danger');
					element.textContent = 'Unlike';
					element.dataset.likes = 'False';
				}
			})
			.catch((error) => {
				console.error('Error:', error);
			});
	};
});

function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = cookies[i].trim();
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === name + '=') {
				cookieValue = decodeURIComponent(
					cookie.substring(name.length + 1)
				);
				break;
			}
		}
	}
	return cookieValue;
}
