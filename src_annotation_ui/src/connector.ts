import { DEVMODE } from './globals'

// let SERVER_LOG_ROOT = DEVMODE ? "http://127.0.0.1/" : "https://quest.ms.mff.cuni.cz/mmsg/"
let SERVER_DATA_ROOT = DEVMODE ? "http://127.0.0.1:9000/queues/" : "https://vilda.net/s/att/queues/"

export async function load_data(): Promise<any> {
    let random_v = `?v=${Math.random()}`;
    let result = await $.ajax(
        SERVER_DATA_ROOT + globalThis.uid + ".jsonl" + random_v,
        {
            type: 'GET',
            contentType: 'application/text',
        }
    )
    result = JSON.parse("[" + result.replaceAll("\n", ",") + "]")
    return result
}

// dumps all the data which is long-term unsustainable but since the image is not part of the payload
// it's expected to be <100k
// export async function log_data(): Promise<any> {
//     let result = await $.ajax(
//         SERVER_LOG_ROOT + "log",
//         {
//             data: JSON.stringify({ data: globalThis.data, uid: globalThis.uid }),
//             type: 'POST',
//             contentType: 'application/json',
//         }
//     )
//     return result
// }