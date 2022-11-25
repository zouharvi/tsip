import { DEVMODE } from "./globals"
export var UID: string
import { load_data } from './connector'
import { setup_navigation, load_cur_text } from "./worker_website"

globalThis.data_i = 0;
globalThis.phase = -1;
globalThis.data = null

globalThis.uid = "onestopqa_apopka"
// const urlParams = new URLSearchParams(window.location.search);
// globalThis.uid = urlParams.get('uid');

// if (globalThis.uid == null) {
//     let UID_maybe = null
//     while (UID_maybe == null) {
//         UID_maybe = prompt("What is your user id?")
//     }
//      // TODO validate
//     globalThis.uid = UID_maybe!;
// }

load_data().then((data: any) => {
    globalThis.data = data
    globalThis.data_now = globalThis.data[globalThis.data_i];
    setup_navigation()
    load_cur_text()
})
