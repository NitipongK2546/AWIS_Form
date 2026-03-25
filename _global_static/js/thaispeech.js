import EasySpeech from 'https://cdn.jsdelivr.net/npm/easy-speech/+esm'

await EasySpeech.init()

// const all_voices = EasySpeech.voices()
// const thai_voice = all_voices.find(voice => voice.lang == "th-TH")
const thai_voice = EasySpeech.filterVoices({
    "language": "th-TH",
    "localSerive": true,
})[0]
console.log(thai_voice)

let thai_text = `
มานีกินปลา มานากินข้าว\n
มาพร้าวกินเนื้อ, มาเขือแม่ปลาบู่ทอง.
ทดสอบสำเร็จ
`

let is_speaking = false

const speak_button = document.getElementById("speak-button")

async function startSpeaking() {
    is_speaking = true

    await EasySpeech.speak({
        "option": {},
        "text": thai_text,
        "voice": thai_voice,
    })

    is_speaking = false
}

speak_button.addEventListener("click", async () => {
    if (!is_speaking) {
        await startSpeaking()
    }
})