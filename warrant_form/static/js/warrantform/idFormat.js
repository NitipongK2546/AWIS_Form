import Inputmask from "https://cdn.jsdelivr.net/npm/inputmask@5.0.9/dist/inputmask.es6.js"

var warrant_id = document.getElementById("id_acc_card_id");

var im = new Inputmask("9-9999-99999-99-9");

im.mask(warrant_id);