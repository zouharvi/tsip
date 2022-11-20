import { DEVMODE } from "./globals"
export var UID: string
import { load_data } from './connector'
import { setup, load_cur_abstract } from "./worker_website"

globalThis.data_i = 0;
globalThis.data = null

// const urlParams = new URLSearchParams(window.location.search);
// globalThis.uid = urlParams.get('uid');

// if (globalThis.uid == null) {
//     let UID_maybe = null
//     while (UID_maybe == null) {
//         UID_maybe = prompt("What is your user id? If none was assigned, make up one with alpha characters of length <= 15.")
//     }
//     globalThis.uid = UID_maybe!
// }

// load_data().then((data: any) => {
//     globalThis.data = data
//     globalThis.data_now = globalThis.data[globalThis.data_i];
//     setup()
//     load_cur_abstract()
// })

