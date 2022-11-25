import { log_data } from "./connector";
import { getIndicies } from "./utils";

let main_text_area = $("#main_simplified_text_area")
let main_answer_area = $("#active_response_area")

function load_headers() {
    $("#progress").html(`
        <strong>Progress:</strong> ${globalThis.data_i + 1}/${globalThis.data.length},
        <strong>UID:</strong> ${globalThis.uid},
        <strong>mode:</strong> ${globalThis.data_now["mode"]}
    `)
}

function update_phase_texts() {
    ["#phase_read", "#phase_answer", "#phase_eval"].forEach((id, index) => {
        let obj = $(id);
        ["phase_progress", "phase_done", "phase_locked"].forEach((val, _) => {
            obj.removeClass(val);
        })


        if (index == globalThis.phase) {
            obj.text("in progress");
            obj.addClass("phase_progress");
        } else if (index < globalThis.phase) {
            obj.text("done");
            obj.addClass("phase_done");
        } else if (index > globalThis.phase) {
            obj.text("locked");
            obj.addClass("phase_locked");
        }
    });
}

function setup_main_text_with_simplifications(text: string) {
    let replacer = new Map<number, string>();
    globalThis.data_now["simplifications"].forEach((val, val_i) => {
        let indicies = getIndicies(val[0], text, true);
        let chunks = [];
        let last_text = text;
        indicies.forEach((index, _) => {
            chunks.push(last_text.slice(0, index));
            last_text = last_text.slice(index);
        })
        chunks.push(last_text);
        replacer[val_i] = val[1];

        text = chunks.map((chunk_text: string, index) => {
            // protect against replacing parts of attributes
            if (index == 0 || chunk_text.slice(0, val[0].length).includes("\"")) {
                return chunk_text;
            }
            return chunk_text.replace(val[0], `<span class="simplify_u" replace_with="${val_i}">` + val[0] + "</span>");
        }).join("")
    });
    main_text_area.html(text);

    $(".simplify_u").each((_, el) => {
        $(el).on("click", () => {
            let replace_with = replacer[Number(el.getAttribute("replace_with"))];
            $(el).html(replace_with);
            $(el).removeClass("simplify_u");
            // refresh triggers
            setup_main_text_with_simplifications(main_text_area.text());
        })
    });
}

function setup_main_text(text: string) {
    main_text_area.html(text);
}

function setup_questions_answers() {
    let output_html = "";
    let questions = globalThis.data_now["questions"];
    questions.forEach(([question, answers], question_i) => {
        output_html += question + "<br> <ol type='A'>";
        answers.forEach((answer, answer_i) => {
            output_html += `<li><input type="radio" name="question_group_${question_i}" id="qa_${question_i}_${answer_i}">`
            output_html += `<label for="qa_${question_i}_${answer_i}">${answer}</label></li>`
        });
        output_html += "</ol>";
    })
    main_answer_area.html(output_html);

    questions.forEach(([question, answers], question_i) => {
        answers.forEach((answer, answer_i) => {
            let radio_el = $(`#qa_${question_i}_${answer_i}`)
            radio_el.on("input checked", (el) => {
                globalThis.data_log.answers_extrinsic[question_i] = answer_i
            })
        })
    })
}

function setup_human_intrinsic() {
    let output_html = "";
    let questions = [
        "How confident are you in your answers?",
        "Did the text provide enough information to answer the questions?",
        "Did the text contain unnecessary information?",
        "What is the complexity of the text?",
        "What is the fluency & grammaticality of the text?",
    ];
    questions.forEach((question, question_i) => {
        output_html += `${question}<br>`
        output_html += `<input class="hi_input_val" type="range" min="0", max="5", step="1" id="val_${question_i}">`
        output_html += `<span class="hi_input_label" id="label_${question_i}">-</span>`
        output_html += "<br><br>"
    });
    main_answer_area.html(output_html);
    questions.forEach((question, question_i) => {
        let range_el = $(`#val_${question_i}`)
        range_el.on("input change", (el) => {
            $(`#label_${question_i}`).text(range_el.val() as string)
            globalThis.data_log.answers_intrinsic[question_i] = range_el.val()
        })
    })
}

function update_text_and_answers() {
    switch (globalThis.phase) {
        case -1:
            main_text_area.html($("#phase_text_before_start").html());
            main_answer_area.text("");
            break;
        case 0:
            setup_main_text(globalThis.data_now["text"]);
            main_answer_area.text("Focus on the reading");
            break;
        case 1:
            setup_questions_answers();
            break;
        case 2:
            setup_human_intrinsic()
            break;
    }
}

function load_cur_text() {
    load_headers()
    update_phase_texts()
    update_text_and_answers()
}

// function load_cur_abstract_all_direct() {
//     title_area_table.html("")
//     title_area_table.append($("<tr><td>Title</td><td>Score</td></tr>"));

//     globalThis.data_now["titles_order"].forEach((title_order: number, title_i: number) => {
//         let new_an = $(`
//             <tr>
//                 <td>• ${globalThis.data_now["titles"][title_order]}</td>
//                 <td><span id="q_${title_i}_val">x</span><input id="q_${title_i}" type="range" min="0" max="4" step="1"></td>
//             </tr>
//         `)
//         title_area_table.append(new_an);
//         bind_labels_direct(title_i);
//     })


//     if (!globalThis.data_now.hasOwnProperty("response")) {
//         globalThis.data_now["response"] = []
//         globalThis.data_now["titles_order"].forEach((title: string) => {
//             // set default response
//             globalThis.data_now["response"].push(-1);
//         });

//         // space for comments
//         globalThis.data_now["response"].push("")
//     }

//     // resets values
//     globalThis.data_now["titles_order"].forEach((title: string, title_i: number) => {
//         $("#q_" + title_i.toString()).val(globalThis.data_now["response"][title_i]);
//     })
// }

function setup_navigation() {
    // progress next
    $("#but_next").on("click", () => {
        globalThis.phase += 1;
        if (globalThis.phase == 0) {
            globalThis.data_log = {
                times: [Date.now()],
                answers_extrinsic: {},
                answers_intrinsic: {},
            }
        } else if (globalThis.phase == 1) {
            // finish reading phase
            globalThis.data_log.times.push(Date.now())
        } else if (globalThis.phase == 2) {
            // finish extrinsic questions phase
            globalThis.data_log.times.push(Date.now())
        } else if (globalThis.phase == 3) {
            // finish intrinsic questions phase
            globalThis.phase = -1;
            globalThis.data_i += 1;

            globalThis.data_log.times.push(Date.now())
            log_data(globalThis.data_log)
        }

        if (globalThis.data_i >= globalThis.data.length) {
            alert("You completed the whole queue, thanks! Wait a few seconds to finish synchronization.");
            globalThis.data_i = 0;
        }

        globalThis.data_now = globalThis.data[globalThis.data_i];
        load_cur_text()
    })
}


export { setup_navigation, load_cur_text }