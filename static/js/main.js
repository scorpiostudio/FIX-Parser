
            function show_time_line(){
                $("#header_line_table>tbody").empty();
                var lines = {{lines|tojson|safe}};
                var skip_admin_messages_checked = $('#skip_admin_messages').prop('checked');
                var skip_heartbeats_checked = $('#skip_heart_beats').prop('checked');
                // 追加FIX消息到TimeLine Table
                for(var i=0; i<lines.length;i++)
                {
                    var line = lines[i];
                    if(skip_admin_messages_checked)
                    {
                        if(line.msgcat == "admin")
                        {
                            continue;
                        }
                    }
                    if(skip_heartbeats_checked)
                    {
                        if(line.message == "Heartbeat")
                        {
                            continue;
                        }
                    }
                    var tr = `<tr align='center' height='30' class=tr_${i} data-trid=${i}>` + "<td>" + line.time + "</td>" + "<td>" + line.sender + "</td>"
                    + "<td>" + line.target + "</td>" + "<td>" + line.message + "</td>" + "<td>" + line.client_order_id + "</td>" +
                    "<td style='word-wrap:break-word;word-break:break-all;'>" + line.details + "</td>" + "</tr>";
                    $("#header_line_table").append(tr);
                }
                // 交替行颜色设置
                $("tr:odd").addClass("tr_odd");
                $("tr:even").addClass("tr_even");

            }

            function show_fix_message(row) {
                // 清空表格tbody
                $("#fix_message>tbody").empty();
                var messages = {{messages|tojson|safe}};
                // 获取第row行的FIX Message
                var message = messages[row];
                var fields = message.fields;
                var isChecked = $('#skip_common_fields').prop('checked');
                // 追加FIX消息的所有Field到FIX Message Table
                for(var i=0; i<fields.length;i++)
                {
                    var ok = false;
                    var tag_name = "<td>" + fields[i].tag_name + "</td>";
                    // 是否过滤common类字段
                    if(isChecked)
                    {
                        for(var j = 0; j < message.common_fields.length; j++)
                        {
                            if(fields[i].tag_name == message.common_fields[j])
                            {
                                tag_name = '<td><font color="green">' + fields[i].tag_name + "</font></td>";
                                ok = true;
                            }
                        }
                    }

                    if(ok)
                    {
                        continue;
                    }
                    var tr = "<tr align='center' height='30'>" + "<td>" + fields[i].tag +
                    "</td>" + tag_name + "<td>" + fields[i].value + "</td>" +
                    "<td style='word-wrap:break-word;word-break:break-all;'>" + fields[i].value_description + "</td>" + "</tr>";
                    $("#fix_message").append(tr);
                }
                // 交替行颜色设置
                $("tr:odd").addClass("tr_odd");
                $("tr:even").addClass("tr_even");
            }
            // 上传文件处理
            function handleFileSelect(event) {
                let reads = new FileReader();
                let file = document.getElementById('fix_file').files[0];
                reads.readAsText(file, 'utf-8');
                reads.onload = function (e) {
                    document.getElementById('input').value = e.target.result
                    $('#input_form').submit();
                };
                $("#fix_file").val("");
            }
            function show_fix_versions(){
                $('#standard_fix').empty();
                var standard_fix_list = {{standard_fix_list|tojson|safe}};
                for(let i = 0; i < standard_fix_list.length; i++)
                {
                    var option = $("<option>").val(standard_fix_list[i]).text(standard_fix_list[i]);
                    $("#standard_fix").append(option);
                }
                $('#custom_fix').empty();
                var custom_fix_list = {{custom_fix_list|tojson|safe}};
                for(let i = 0; i < custom_fix_list.length; i++)
                {
                    var option = $("<option>").val(custom_fix_list[i]).text(custom_fix_list[i]);
                    $("#custom_fix").append(option);
                }
            }

