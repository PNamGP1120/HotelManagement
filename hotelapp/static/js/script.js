const avatarButton = document.querySelector('.avatar-button');
const dropdownMenu = document.querySelector('.dropdown-menu');

avatarButton.addEventListener('click', () => {
  dropdownMenu.classList.toggle('show');
});