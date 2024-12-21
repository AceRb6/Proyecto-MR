const byId=(id)=> {
    return document.getElementById(id);
};
const $signUpbutton=byId('signUp');
const $signInbutton=byId('signIn');
const $container=byId('container');

$signUpbutton.addEventListener(
    'click',
    ()=>{
        $container.classList.add('right-panel-active');
    },
);

$signInbutton.addEventListener(
    'click',
    ()=>{
        $container.classList.remove('right-panel-active');
    },
);