const toggleElement = (element) => {
    if (element.classList.contains(HIDE_CLASS)) {
        element.classList.remove(HIDE_CLASS);
    } else {
        element.classList.add(HIDE_CLASS);
    }
}

const toggleGameSettingsView = () => {
    toggleElement(document.querySelector('.js-game-settings'));
};

const toggleGameView = () => {
    toggleElement(document.querySelector('.js-game'));
};

const toggleEndGameLostView = () => {
    toggleElement(document.querySelector('.js-end-game-lost'));
};

const toggleEndGameWinView = () => {
    toggleElement(document.querySelector('.js-end-game-win'));
};

const hideEndGameView = () => {
    const endGameWin = document.querySelector('.js-end-game-win');
    const endGameLost = document.querySelector('.js-end-game-lost');

    if (!endGameWin.classList.contains(HIDE_CLASS)) { endGameWin.classList.add(HIDE_CLASS); }
    if (!endGameLost.classList.contains(HIDE_CLASS)) { endGameLost.classList.add(HIDE_CLASS); }
}