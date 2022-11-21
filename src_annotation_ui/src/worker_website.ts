let title_area_table = $("#title_area_table_body")

function load_headers() {
    $("#progress").html(`
        <strong>Progress:</strong> ${globalThis.data_i + 1}/${globalThis.data.length},
        <strong>UID:</strong> ${globalThis.uid},
        <strong>mode:</strong> ${globalThis.data_now["mode"]}
    `)
    $("#main_simplified_text_area").text(globalThis.data_now["text"])
}

function update_phase_texts() {
    ["#phase_read", "#phase_answer", "#phase_eval"].forEach((id, index) => {
        let obj = $(id);
        ["phase_progress", "phase_done", "phase_locked"].forEach((val, _) => {
            obj.removeClass(val);
        })
        if (index == globalThis.phase) {
            obj.html("<b>in progress</b>");
        } else if (index < globalThis.phase) {
            obj.html("done");
        } else if (index > globalThis.phase) {
            obj.html("locked");
        }
    });
}

function load_cur_text() {
    load_headers()

    update_phase_texts()
    $("#phase_read").prop("disabled", true);

    // TODO
    // load_cur_abstract_all_direct();    
}

function load_cur_abstract_all_direct() {
    title_area_table.html("")
    title_area_table.append($("<tr><td>Title</td><td>Score</td></tr>"));

    globalThis.data_now["titles_order"].forEach((title_order: number, title_i: number) => {
        let new_an = $(`
            <tr>
                <td>• ${globalThis.data_now["titles"][title_order]}</td>
                <td><span id="q_${title_i}_val">x</span><input id="q_${title_i}" type="range" min="0" max="4" step="1"></td>
            </tr>
        `)
        title_area_table.append(new_an);
        bind_labels_direct(title_i);
    })


    if (!globalThis.data_now.hasOwnProperty("response")) {
        globalThis.data_now["response"] = []
        globalThis.data_now["titles_order"].forEach((title: string) => {
            // set default response
            globalThis.data_now["response"].push(-1);
        });

        // space for comments
        globalThis.data_now["response"].push("")
    }

    // resets values
    globalThis.data_now["titles_order"].forEach((title: string, title_i: number) => {
        $("#q_" + title_i.toString()).val(globalThis.data_now["response"][title_i]);
    })
}

function bind_labels_direct(title_i: number) {
    $("#q_" + title_i.toString()).on('input change', function () {
        let val = parseInt($(this).val() as string);
        globalThis.data_now["response"][title_i] = val;

        let slider_obj_val = $("#q_" + title_i.toString() + "_val");
        slider_obj_val.text(val)
    });

    // special handling of default "empty" value
    $("#q_" + title_i.toString()).on('click', function () {
        if (globalThis.data_now["response"][title_i] == -1) {
            globalThis.data_now["response"][title_i] = 0;

            let val = parseInt($(this).val() as string);
            console.log(val)
            let slider_obj_val = $("#q_" + title_i.toString() + "_val");
            slider_obj_val.text(val)
        }
    });
}


function setup_navigation() {
    // send current data
    // load next abstract
    $("#but_next").on("click", () => {
        globalThis.phase += 1;
        if (globalThis.phase >= 3) {
            globalThis.phase = 0;
            globalThis.data_i += 1;
        }

        if (globalThis.data_i >= globalThis.data.length) {
            alert("You completed the whole queue, thanks! Wait a few seconds to finish synchronization.");
            globalThis.data_i = 0;
        }

        globalThis.data_now = globalThis.data[globalThis.data_i];
        // log_data()
        load_cur_text()
    })

    // $("#but_prev").on("click", () => {
    //     globalThis.data_i -= 1;
    //     // modulo
    //     if (globalThis.data_i < 0) {
    //         globalThis.data_i = globalThis.data.length - 1;
    //     }

    //     globalThis.data_now = globalThis.data[globalThis.data_i];
    //     // log_data()
    //     load_cur_text()
    // })
}


export { setup_navigation, load_cur_text }