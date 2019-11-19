            function show_time_line(messages){
                // 清空表格tbody
                $("#header_line_table>tbody").empty();
                // 读取服务端返回的lines
                var skip_admin_messages_checked = $('#skip_admin_messages').prop('checked');
                var skip_heartbeats_checked = $('#skip_heart_beats').prop('checked');
                var text = ''
                // 追加FIX消息到TimeLine Table
                for(var i=0; i<lines.length;i++)
                {
                    var line = lines[i];
                    text = text + line.raw + '\n'
                    // 是否过滤管理类消息
                    if(skip_admin_messages_checked)
                    {
                        if(line.msgcat == "admin")
                        {
                            continue;
                        }
                    }
                    // 是否过滤心跳消息
                    if(skip_heartbeats_checked)
                    {
                        if(line.message == "Heartbeat")
                        {
                            continue;
                        }
                    }
                    id_td = '<td>' + line.id + "</td>"
                    message_td = '<td>' + line.message + "</td>"
                    if(line.msgcat == "admin")
                    {
                        message_td = '<td><span class="Time_Line_Span"  onclick="click_span()" style="background:#CCCCCC">'+ line.message + "</span></td>"
                    }

                    if(line.message == "Reject")
                    {
                        message_td = '<td><span class="Time_Line_Span"  onclick="click_span()" style="background:red">'+ line.message + "</span></td>"
                    }
                    if(line.message == "NewOrderSingle")
                    {
                        message_td = '<td><span class="Time_Line_Span"  onclick="click_span()" style="background:green">'+ line.message + "</span></td>"
                    }
                    var tr = `<tr align='center' height='30' class=tr_${i} data-trid=${i}>` + id_td + "<td>" + line.time + "</td>" + "<td>" + line.sender + "</td>"
                    + "<td>" + line.target + "</td>" + message_td + "<td>" + line.client_order_id + "</td>" +
                    "<td style='word-wrap:break-word;word-break:break-all;'>" + line.details + "</td>" + "</tr>";
                    $("#header_line_table").append(tr);
                }
                document.getElementById('input').value = text
                // 交替行颜色设置
                $("tr:odd").addClass("tr_odd");
                $("tr:even").addClass("tr_even");
            }

            function show_fix_message(row, messages) {
                // 清空表格tbody
                $("#fix_message>tbody").empty();
                // 获取第row行的FIX Message
                var message = messages[row];
                var fields = message.fields;
                var isChecked = $('#skip_common_fields').prop('checked');
                // 追加FIX消息的所有Field到FIX Message Table
                for(var i=0; i<fields.length;i++)
                {
                    // 是否过滤common类字段
                    var field = fields[i]
                    if(isChecked)
                    {
                        if(field[3] == 'True')
                        {
                           continue;
                        }
                    }
                    var tag_name = "<td>" + field[2] + "</td>";
                    if(field[3] == 'True')
                    {
                        tag_name = '<td><span style="background-color:#CCCCCC">' + field[2] + "</span></td>";
                    }
                    var tr = "<tr align='center' height='30'>" + "<td>" + field[0] +
                    "</td>" + tag_name + "<td>" + field[1] + "</td>" +
                    "<td style='word-wrap:break-word;word-break:break-all;'>" + field[4] + "</td>" + "</tr>";
                    $("#fix_message").append(tr);
                }
                // 交替行颜色设置
                $("tr:odd").addClass("tr_odd");
                $("tr:even").addClass("tr_even");
            }

            // 显示FIX协议版本选择
            function show_fix_versions(standard_fix_list, custom_fix_list){
                $('#standard_fix').empty();
                for(let i = 0; i < standard_fix_list.length; i++)
                {
                    var option = $("<option>").val(standard_fix_list[i]).text(standard_fix_list[i]);
                    $("#standard_fix").append(option);
                }
                $('#custom_fix').empty();
                for(let i = 0; i < custom_fix_list.length; i++)
                {
                    var option = $("<option>").val(custom_fix_list[i]).text(custom_fix_list[i]);
                    $("#custom_fix").append(option);
                }
            }

        var files = [];
//        $(document).ready(function(){
//            $('#fix_file').change(function () {
//                    files = this.files;
//                })
//            $("tr:odd").addClass("tr_odd");
//            $("tr:even").addClass("tr_even");
//            var fix_version = {{ fix_version|tojson|safe }};
//            show_fix_versions();
//            $("#fix_version_select").val(fix_version);
//        })

        $("#upload_file").click(function () {
            var form_data = new FormData($('#input_form')[0]);
            for (var i = 0; i < files.length; i++) {
                form_data.append("file", files[i]);
            }
            var index = document.getElementById('fix_version_select').selectedIndex;
            var val = document.getElementById('fix_version_select').options[index].value;
            form_data.append("fix_version_select", val)
            form_data.append("input", $('#input').value)
            $.ajax({
                url:"",
                method: 'POST',
                data: form_data,
                contentType: false,
                processData: false,
                cache: false,
                success: function (msg) {
                    window.location.href="{{ url_for('query') }}";
                    show_time_line();
                    // 设置第1行为当前行
                    $("#header_line_table tr:eq(1)").toggleClass("focus");
                }
            });
        })

        var row = 0;
        const selectEvent = (ele) => {
            let target = event.target
        }

        $('.class_tbody').click(() => {
            let target = event.target.parentElement
            let focusEle = $(target).parent().find("tr.focus")
            focusEle.toggleClass("focus");
            focusEle.unbind('click')
            let trId = target.dataset.trid
            let ele = $(`.tr_${trId}`)
            ele.click(selectEvent(event))

            ele.toggleClass("focus");
            row = trId
            show_fix_message(row);
        })

        function click_span(){
            let target = event.target.parentElement.parentElement
            let focusEle = $(target).parent().find("tr.focus")
            focusEle.toggleClass("focus");
            focusEle.unbind('click')

            let trId = target.dataset.trid
            let ele = $(`.tr_${trId}`)
            ele.click(selectEvent(event))

            ele.toggleClass("focus");
            row = trId
            show_fix_message(row);
            // 阻止事件向上传播
            event.stopPropagation();
        }

        // 点击Time Line表格的skip_admin_messages复选框
        $("#skip_admin_messages").click(function() {
            show_time_line();
            $("#header_line_table tr:eq(1)").toggleClass("focus");
            show_fix_message(0);
        });

        // 点击Time Line表格的skip_heart_beats复选框
        $("#skip_heart_beats").change(function() {
            show_time_line();
            $("#header_line_table tr:eq(1)").toggleClass("focus");
            show_fix_message(0);
        });

        // 点击FIX Message表格的skipCommonFields复选框
        $("#skip_common_fields").change(function() {
            show_fix_message(row);
        });

        $('#parse_fix').click(function() {
            $('#input_from').submit();
        });

        $("#clear").click(function(){
            document.getElementById("input").value = ""
            $("#header_line_table>tbody").empty();
            $("#fix_message>tbody").empty();
        })

        var SAMPLE_FIX_MESSAGES = "8=FIX.4.19=6135=A34=149=EXEC52=20121105-23:24:0656=BANZAI98=0108=3010=003\
            8=FIX.4.19=6135=A34=149=BANZAI52=20121105-23:24:0656=EXEC98=0108=3010=003\
            8=FIX.4.19=4935=034=249=BANZAI52=20121105-23:24:3756=EXEC10=228\
            8=FIX.4.19=4935=034=249=EXEC52=20121105-23:24:3756=BANZAI10=228\
            8=FIX.4.19=10335=D34=349=BANZAI52=20121105-23:24:4256=EXEC11=135215788257721=138=1000040=154=155=MSFT59=010=062\
            8=FIX.4.19=13935=834=349=EXEC52=20121105-23:24:4256=BANZAI6=011=135215788257714=017=120=031=032=037=138=1000039=054=155=MSFT150=2151=010=059\
            8=FIX.4.19=15335=834=449=EXEC52=20121105-23:24:4256=BANZAI6=12.311=135215788257714=1000017=220=031=12.332=1000037=238=1000039=254=155=MSFT150=2151=010=230\
            8=FIX.4.19=10335=D34=449=BANZAI52=20121105-23:24:5556=EXEC11=135215789503221=138=1000040=154=155=ORCL59=010=047\
            8=FIX.4.19=13935=834=549=EXEC52=20121105-23:24:5556=BANZAI6=011=135215789503214=017=320=031=032=037=338=1000039=054=155=ORCL150=2151=010=049\
            8=FIX.4.19=15335=834=649=EXEC52=20121105-23:24:5556=BANZAI6=12.311=135215789503214=1000017=420=031=12.332=1000037=438=1000039=254=155=ORCL150=2151=010=220\
            8=FIX.4.19=10835=D34=549=BANZAI52=20121105-23:25:1256=EXEC11=135215791235721=138=1000040=244=1054=155=SPY59=010=003\
            8=FIX.4.19=13835=834=749=EXEC52=20121105-23:25:1256=BANZAI6=011=135215791235714=017=520=031=032=037=538=1000039=054=155=SPY150=2151=010=252\
            8=FIX.4.19=10435=F34=649=BANZAI52=20121105-23:25:1656=EXEC11=135215791643738=1000041=135215791235754=155=SPY10=198\
            8=FIX.4.19=8235=334=849=EXEC52=20121105-23:25:1656=BANZAI45=658=Unsupported message type10=000\
            8=FIX.4.19=10435=F34=749=BANZAI52=20121105-23:25:2556=EXEC11=135215792530938=1000041=135215791235754=155=SPY10=197\
            8=FIX.4.19=8235=334=949=EXEC52=20121105-23:25:2556=BANZAI45=758=Unsupported message type10=002\
            8=FIX.4.19=6135=A49=INVMGR56=BRKR34=152=20000426-12:05:0698=0108=3010=157\
            8=FIX.4.1,9=61,35=A,49=INVMGR,56=BRKR,34=1,52=20000426-12:05:06,98=0,108=30,10=157,\
            8=FIX.4.2|9=157|35=V|34=2|49=BRKR|52=20120921-06:41:04.295|56=QUOTE1-T|262=1:TOP:EURUSD|263=1|264=1|265=0|266=Y|146=1|55=EUR/USD|460=4|267=2|269=0|269=1|10=170|\
            8=FIX.4.3;9=61;35=A;49=BRKR;56=INVMGR;98=0;34=1;52=20000426-12:05:08;108=30;10=143;\
            8=FIX.4.4^A9=61^A35=A^A49=BRKR^A56=INVMGR^A98=0^A34=1^A52=20000426-12:05:08^A108=30^A10=143^A";

        // Sample Data按钮点击事件处理函数
        $("#sample_data").click(function(){
            document.getElementById("input").value = SAMPLE_FIX_MESSAGES;
            $('#input_form').submit();
        });