import { log_data } from "./connector";
import { DEVMODE } from "./globals";
import { getIndicies } from "./utils";
import Sortable from "sortablejs";

let main_text_area = $("#main_simplified_text_area")
let main_answer_area = $("#active_response_area")

function load_headers() {
    $("#progress").html(`
        <strong>Progress:</strong> ${globalThis.data_i + 1}/${globalThis.data.length},
        <strong>UID:</strong> ${globalThis.uid}
        `)
    // <strong>mode:</strong>${globalThis.data_now["simplification_type"]}
}

function update_phase_texts() {
    ["#phase_task", "#phase_eval"].forEach((id, index) => {
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

function setup_text() {
    main_text_area.html(globalThis.data_now["text"]);
}

function setup_questions_answers() {
    setup_text()

    let output_html = "";
    let questions = globalThis.data_now["task_data"];
    questions.forEach((question, question_i) => {
        let answers = question["answers"]
        answers.push("the question is not answerable from the text");
        output_html += question["text"] + "<br> <ol type='A'>";
        answers.forEach((answer: string, answer_i: number) => {
            output_html += `<li><input type="radio" name="question_group_${question_i}" id="qa_${question_i}_${answer_i}">`
            output_html += `<label for="qa_${question_i}_${answer_i}">${answer}</label></li>`
        });
        output_html += "</ol>";
    })
    main_answer_area.html(output_html);

    questions.forEach((question, question_i) => {
        question["answers"].forEach((answer: string, answer_i: number) => {
            let radio_el = $(`#qa_${question_i}_${answer_i}`)
            radio_el.on("input checked", (el) => {
                globalThis.data_log.answers_extrinsic[question_i] = answer_i;
                check_next_lock_status();
            })
        })
    })
}

function setup_ordering() {
    let sentences: Array<string> = globalThis.data_now["task_data"]["sentences"]
    main_text_area.html("Reorder the sentences into correct order (dragging).");

    let output_html = "<ol id='sentence_list'>";
    output_html += sentences.map((val: string, val_i: number) => `<li sent_i=${val_i}>${val}</li>`).join("\n")
    output_html += "</ol>"
    main_answer_area.html(output_html);

    Sortable.create(
        $('#sentence_list').get(0),
        {
            animation: 150,
            ghostClass: 'blue-background-class',
            onUpdate: function (evt) {
                // store the new ordering
                let sentence_list = $("#sentence_list").children()
                let sentence_order = sentence_list.map((_, domElement: HTMLElement) => parseInt(domElement.getAttribute("sent_i"))).toArray()
                globalThis.data_log.answers_extrinsic = sentence_order
                check_next_lock_status();
            },
        }
    );
}

function setup_task() {
    if (globalThis.data_now["task"] == "reading") {
        setup_questions_answers();
    } else if (globalThis.data_now["task"] == "ordering") {
        setup_ordering()
    } else {
        throw Error(`Unknown task ${globalThis.data_now["task"]}`)
    }
}

const QUESTIONS_HI = {
    "confidence": "How confident are you in your answers?",
    "complexity": "How easy was the text to read? (opposite of complexity)",
    "fluency": "How much was the text fluent and grammatical?",
    // "Did the text provide enough information to answer the questions?",
    // "Was the information in the text was important and necessary?",
}
const QUESTIONS_HI_KEYS = ["confidence", "fluency", "complexity"]

function setup_human_intrinsic() {
    let output_html = "";
    QUESTIONS_HI_KEYS.forEach((question_key) => {
        output_html += `${QUESTIONS_HI[question_key]}<br>`
        output_html += `<input class="hi_input_val" type="range" min="0", max="5", step="1" id="val_${question_key}">`
        output_html += `<span class="hi_input_label" id="label_${question_key}">-</span>`
        output_html += "<br><br>"
    });
    main_answer_area.html(output_html);
    QUESTIONS_HI_KEYS.forEach((question_key) => {
        let range_el = $(`#val_${question_key}`)
        range_el.on("click", (el) => {
            if (!Object.keys(globalThis.data_log.answers_intrinsic).includes(`${question_key}`)) {
                console.log("Clicked the middle for the first time. Setting it to the default value.")
                range_el.val("3");
                range_el.trigger("input");
            }
        });
        range_el.on("input change", (el) => {
            $(`#label_${question_key}`).text(range_el.val() as string);
            globalThis.data_log.answers_intrinsic[question_key] = parseInt(range_el.val() as string);
            check_next_lock_status();
        });
    })
}

function update_text_and_answers() {
    switch (globalThis.phase) {
        case -1:
            main_text_area.html($("#phase_text_before_start").html());
            main_answer_area.text("");
            break;
        case 0:
            setup_task();
            break;
        case 1:
            // make sure the original text is visible
            setup_text()
            setup_human_intrinsic()
            break;
    }
    check_next_lock_status()
}

function load_cur_text() {
    load_headers()
    update_phase_texts()
    update_text_and_answers()
}

function load_thankyou() {
    // TODO: wait for data sync
    load_headers()
    update_phase_texts()
    let html_text = `Thank you for participating in our study. `;
    if (globalThis.uid.startsWith("matism")) {
        html_text += `<br>Please click <a href="https://app.prolific.co/submissions/complete?cc=TODO">this link</a> to go back to Prolific. `
        html_text += `Alternatively use this code <em>TODO</em>.`
    }
    main_text_area.html(html_text);

    main_answer_area.text("");
    $("#but_next").prop("disabled", true);
}

function check_next_lock_status() {
    let target = 0;
    let answered = 0;
    switch (globalThis.phase) {
        case 0:
            answered = Object.keys(globalThis.data_log["answers_extrinsic"]).length;
            if (globalThis.data_now["task"] == "reading") {
                target = globalThis.data_now["task_data"].length
            } else if (globalThis.data_now["task"] == "ordering") {
                // require at least one interaction
                target = 1
            }
            break;
        case 1:
            answered = Object.keys(globalThis.data_log["answers_intrinsic"]).length;
            target = QUESTIONS_HI_KEYS.length
            break;
    }

    $("#but_next").prop("disabled", target > answered && !DEVMODE);
}

function setup_navigation() {
    // progress next
    $("#but_next").on("click", () => {
        globalThis.phase += 1;
        if (globalThis.phase == 0) {
            console.log("Starting new log object")
            globalThis.data_log = {
                times: [Date.now()],
                answers_extrinsic: {},
                answers_intrinsic: {},
                id: globalThis.data_now["id"],
                simplification_type: globalThis.data_now["simplification_type"],
                task: globalThis.data_now["task"],
                task_data: globalThis.data_now["task_data"],
                uid: globalThis.uid,
            }
        } else if (globalThis.phase == 1) {
            // finish extrinsic questions phase
            globalThis.data_log.times.push(Date.now())
        } else if (globalThis.phase == 2) {
            // finish intrinsic questions phase
            globalThis.phase = -1;
            globalThis.data_i += 1;

            globalThis.data_log.times.push(Date.now())
            log_data(globalThis.data_log)
        }

        if (globalThis.data_i >= globalThis.data.length) {
            globalThis.data_i = 0;
            load_thankyou()
        } else {
            globalThis.data_now = globalThis.data[globalThis.data_i];
            load_cur_text()
        }
    })
}


export { setup_navigation, load_cur_text }