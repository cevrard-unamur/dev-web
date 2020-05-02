const settings = {
    life: 0,
    widthGrid: 0,
    heightGrid: 0,
    word: "",
    isPreview: false
};
const HIDE_CLASS = 'hide';
const ROTATE_FLIP_BOX_CLASS = 'flip-box-rotate';
const VISIBILITY_TIME = 3000;

let hm_playedLetters = [];
let hm_isPlaying = false;
let mm_imagemap = [];
let mm_selectedImage1 = null;
let mm_selectedImage2 = null;
let mm_boxFlipped = 0;
let mm_imagespath = [];
let remainingLifes = -1;

const drawHandmanAnswer = () => {
    const wordElement = document.querySelector('.js-word');
    removeAllChild(wordElement);

    for (const letter of settings.word) {
        const spanElement = document.createElement('SPAN');
        if (hm_playedLetters.indexOf(letter) === -1) {
            spanElement.innerHTML = '_';
        } else {
            spanElement.innerHTML = letter;
        }
        wordElement.appendChild(spanElement);
    }
};

const drawPlayedLetters = () => {
    const lettersElement = document.querySelector('.js-letters');
    removeAllChild(lettersElement);

    for (const letter of hm_playedLetters) {
        if (settings.word.indexOf(letter) === -1) {
            const spanElement = document.createElement('SPAN');
            spanElement.innerHTML = letter;
            lettersElement.appendChild(spanElement);
        }
    }
};

const drawReamingLifes = () => {
    const lifesElement = document.querySelector('.js-lifes');
    removeAllChild(lifesElement);

    for (let index = 0; index < remainingLifes; index++) {
        const imageElement = document.createElement('IMG');
        imageElement.src = 'assets/life.png';
        imageElement.alt = 'Une vie restante';
        lifesElement.appendChild(imageElement);
    }
};

const disabledHandmanSection = (status) => {
    document.querySelector('.js-guess').disabled = status;
    document.querySelector('.js-guess-button').disabled = status;
};

const findHandmanLetter = () => {
    hm_isPlaying = false;
    disabledHandmanSection(true);

    const guessElement = document.querySelector('.js-guess');

    // We check the validity of the value
    if (guessElement.value.length !== 1 ||
        hm_playedLetters.indexOf(guessElement.value) !== -1) {
        remainingLifes--;
        guessElement.disabled = true;
        event.target.disabled = true;
    } else {
        guessElement.value = guessElement.value.toLowerCase();
        hm_playedLetters.push(guessElement.value);

        // We check if the input isin the word to guess
        if (settings.word.indexOf(guessElement.value) === -1) {
            remainingLifes--;
            guessElement.disabled = true;
            event.target.disabled = true;
        }
    }

    drawHandmanAnswer();
    drawPlayedLetters();
    drawReamingLifes();

    guessElement.value = '';

    // If there is no reaming lives or boz to flip, the game is lost.
    if (remainingLifes === 0 || mm_imagemap.length - mm_boxFlipped === 0) {
        toggleEndGameLostView();
        toggleGameView();
    } else {
        // We check if the player has found all the letters of the word.
        let isGameWin = true;

        for (const letter of settings.word) {
            if (hm_playedLetters.indexOf(letter) === -1) {
                isGameWin = false;
            }
        }

        if (isGameWin) {
            toggleEndGameWinView();
            toggleGameView();
        }
    }
};

const rotateFlipBoxEvent = (event) => {
    // We get the flip box element.
    let flipBoxElement = event.target;

    do {
        flipBoxElement = flipBoxElement.parentElement;
    } while (!flipBoxElement.classList.contains('flip-box'))

    // If the box is already rotate, we cannot select it again
    if (flipBoxElement.classList.contains(ROTATE_FLIP_BOX_CLASS) ||
        (mm_selectedImage1 !== null && mm_selectedImage2 !== null) ||
        hm_isPlaying) {
        return;
    }

    // We rotate the selected box
    flipBoxElement.classList.add(ROTATE_FLIP_BOX_CLASS);

    // We save the selected box
    if (mm_selectedImage1 === null) {
        mm_selectedImage1 = flipBoxElement;
    } else {
        mm_selectedImage2 = flipBoxElement;
    }

    // If we have two selected boxes, we check if they are showing the same image
    if (mm_selectedImage1 !== null && mm_selectedImage2 !== null) {
        const srcImage1 = mm_selectedImage1.querySelector('.js-memory-image').src;
        const srcImage2 = mm_selectedImage2.querySelector('.js-memory-image').src;

        if (srcImage1 === srcImage2) {
            // We have the same image, we can play with the handman game
            mm_selectedImage1 = null;
            mm_selectedImage2 = null;
            mm_boxFlipped += 2;
            hm_isPlaying = true;
            disabledHandmanSection(false);
        } else {
            remainingLifes--;
            drawReamingLifes();

            setTimeout(() => {
                // We hide the two images and remove a life
                // and reset the value of selected images to the default one
                mm_selectedImage1.classList.remove(ROTATE_FLIP_BOX_CLASS);
                mm_selectedImage2.classList.remove(ROTATE_FLIP_BOX_CLASS);
                mm_selectedImage1 = null;
                mm_selectedImage2 = null;

                // If there is no remaining lives, the game is lost
                if (remainingLifes === 0) {
                    toggleEndGameLostView();
                    toggleGameView();
                }
            }, VISIBILITY_TIME)
        }
    }
}

const drawMemoryMap = () => {
    // We take the imges we need to match the settings of the users
    // We divide per 2 as we will need to duplicate all selected images
    let neededImages = (settings.widthGrid * settings.heightGrid) / 2;

    for (let index = 1; index <= neededImages; index++) {
        mm_imagemap.push(mm_imagespath[index % mm_imagespath.length]);
    }

    // We duplicate every images
    mm_imagemap = [
        ...mm_imagemap,
        ...mm_imagemap
    ];

    // We shuffle them
    mm_imagemap = shuffle(mm_imagemap);

    // We add the images to the view
    const memoryMapElement = document.querySelector('.js-memory-map');
    removeAllChild(memoryMapElement);

    /*
     * HTML structure of a memory element
     *   The image is set two times to have a correct height when the image to found is not display

     <div class="flip-box img-mermory-XX">
        <div class="flip-box-inner">
            <img src="assets/memory/img-1.png">
            <div class="flip-box-front">
            </div>
            <div class="flip-box-back">
                <img src="assets/memory/img-1.png">
            </div>
        </div>
    </div>
     */

    for (const imagemap of mm_imagemap) {

        const flipBoxElement = document.createElement('DIV');
        flipBoxElement.classList.add('flip-box');
        flipBoxElement.classList.add(ROTATE_FLIP_BOX_CLASS); // We had this class to preview the element of the memory
        flipBoxElement.classList.add(`img-mermory-${settings.widthGrid}`);
        // We have the event to play the memoy game
        flipBoxElement.addEventListener('click', rotateFlipBoxEvent);

        const flipBoxInnerElement = document.createElement('DIV');
        flipBoxInnerElement.classList.add('flip-box-inner');
        const imageInnerElement = document.createElement('IMG');
        imageInnerElement.classList.add('js-memory-image'); // This class is use to get the selected image
        imageInnerElement.src = imagemap;

        const flipBoxFrontElement = document.createElement('DIV');
        flipBoxFrontElement.classList.add('flip-box-front');
        const flipBoxBackElement = document.createElement('DIV');
        flipBoxBackElement.classList.add('flip-box-back');
        const imageBackElement = document.createElement('IMG');
        imageBackElement.src = imagemap;

        flipBoxBackElement.appendChild(imageBackElement);
        flipBoxInnerElement.appendChild(imageInnerElement);
        flipBoxInnerElement.appendChild(flipBoxFrontElement);
        flipBoxInnerElement.appendChild(flipBoxBackElement);
        flipBoxElement.appendChild(flipBoxInnerElement);
        memoryMapElement.appendChild(flipBoxElement);
    }

    setTimeout(() => {
        const flipBoxElements = document.querySelectorAll('.flip-box');
        for (const flipBoxElement of flipBoxElements) {
            flipBoxElement.classList.remove('flip-box-rotate');
        }
    }, settings.isPreview ? VISIBILITY_TIME : 0);
};

// Launch the game
document.querySelector('.js-play').addEventListener('click', (event) => {
    event.preventDefault();

    document.querySelector('.js-error').innerHTML = '';

    settings.life = document.getElementById('life').value;
    settings.widthGrid = document.getElementById('width-grid').value;
    settings.heightGrid = document.getElementById('height-grid').value;
    settings.word = document.getElementById('word').value.toLowerCase();
    settings.isPreview = document.getElementById('preview').checked;

    if (settings.heightGrid * settings.widthGrid % 2 !== 0) {
        document.querySelector('.js-error').innerHTML = 'La largeur multipliée par la hauteur de la carte doit donner un nombre pair.';
        return;
    }

    if ((settings.heightGrid * settings.widthGrid / 2) < settings.word.length) {
        document.querySelector('.js-error').innerHTML = 'Il n\'y a pas assez de case pour pouvoir gagner.';
        return;
    }

    if (settings.widthGrid > 15) {
        document.querySelector('.js-error').innerHTML = 'La largeur de la carte ne peut être supérieur à 15.';
        return;
    }

    // Initialize the images for the memory
    for (let index = 1; index <= 24; index++) {
        mm_imagespath.push(`assets/memory/img-${index}.png`);
    }

    remainingLifes = settings.life;

    toggleGameSettingsView();
    toggleGameView();

    drawHandmanAnswer();
    drawPlayedLetters();
    drawReamingLifes();
    drawMemoryMap();

    disabledHandmanSection(true);
});

// Handman game
document.querySelector('.js-guess').addEventListener('keyup', (event) => {
    if (event.keyCode === 13) {
        findHandmanLetter();
    }
});
document.querySelector('.js-guess-button').addEventListener('click', findHandmanLetter);

const restartButtonElements = document.querySelectorAll('.js-restart');
for (const restartButtonElement of restartButtonElements) {
    restartButtonElement.addEventListener('click', () => {
        hm_playedLetters = [];
        hm_isPlaying = false;
        mm_imagemap = [];
        mm_selectedImage1 = null;
        mm_selectedImage2 = null;
        mm_boxFlipped = 0;
        remainingLifes = -1;

        hideEndGameView();
        toggleGameSettingsView();
    });
}