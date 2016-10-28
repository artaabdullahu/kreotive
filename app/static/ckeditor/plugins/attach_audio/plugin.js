/*
 Author - Sahil Batla
 Contact - sahilbathla1@gmail.com
 Description - This plugins provides a basic iframe to upload attachments
 Configs while using in editor -
 1) AutoClose -  To auto close dialog on upload (autoClose: true)
 2) Callback on attachment upload - onAttachmentUpload: function() {}
 3) validateSize - Validate size of file before upload (validateSize: 30) i.e 30mb limit
 */
audioAttachmentUploader = {
    uploadAudioButton: null,
    editor: null,
    uploadEventBinded: false,
    uploadingContainer: null,
    statusMessageContainer: null,
    uploadingSource: CKEDITOR.plugins.getPath('attach_audio') + 'uploading.gif',
    autoClose: false,
    validateSize: 0,
    setStatusMessageContainer: function (_this) {
        this.statusMessageContainer = _this.getElement();
    },
    setUploadingContainer: function (_this) {
        this.uploadingContainer = _this.getElement()
    },
    setAudioUploadButton: function (_this) {
        this.uploadAudioButton = $(_this.getInputElement().$.children[0]);
    },
    getFileField: function () {
        return $($('body').find('iframe.cke_dialog_ui_input_file:visible').contents().find('input[type="file"]'));
    },
    getResultantHTML: function () {
        return $($('div[name=UploadAudio] table tbody > tr:nth-child(2) td div iframe.cke_dialog_ui_input_file').contents().find('body')).text()
    },
    bindUploadEvent: function () {
        //Handle iframe redirect
        var uploadHandler = function () {
            if (audioAttachmentUploader.uploadAudioButton.text() == 'Uploading..') {
                //Provide onAttachmentUpload Callback after upload
                //Define this function in CKEDITOR config
                if (audioAttachmentUploader.editor.config.onAttachmentUpload) {
                    audioAttachmentUploader.editor.config.onAttachmentUpload(audioAttachmentUploader.getResultantHTML());
                }
                audioAttachmentUploader.uploadAudioButton.text('Uploaded');
                audioAttachmentUploader.statusMessageContainer.setText('File Upload Successful!!');
                audioAttachmentUploader.statusMessageContainer.show();
                audioAttachmentUploader.uploadingContainer.hide();
                if (audioAttachmentUploader.autoClose) {
                    CKEDITOR.dialog.getCurrent().hide();
                }
            }
        }
        $('body').find('iframe.cke_dialog_ui_input_file').load(uploadHandler);
        audioAttachmentUploader.uploadEventBinded = true;
    }
}

CKEDITOR.dialog.add('abbrDialogsAudio', function (editor) {
    return {
        title: 'Upload Audio',
        minWidth: 400,
        minHeight: 200,

        contents: [
            {
                id: 'UploadAudio',
                filebrowser: 'uploadButton',
                hidden: true,
                elements: [
                    {
                        type: 'html',
                        html: 'Please upload a single file, zip and upload multiple files if required'
                    },
                    {
                        type: 'file',
                        id: 'attachment',
                        inputStyle: 'outline: 0',
                        style: 'height:40px',
                        size: 38,
                    },
                    {
                        type: 'fileButton',
                        id: 'uploadButton',
                        filebrowser: 'info:txtUrl',
                        label: editor.lang.image.btnUpload,
                        'for': ['UploadAudio', 'attachment'],
                        onClick: function () {
                            var attachment = audioAttachmentUploader.getFileField();
                            if (attachment.val()) {
                                if (audioAttachmentUploader.validateSize > 0 && attachment[0].files[0].size > audioAttachmentUploader.validateSize * 1000000) {
                                    alert('File Size Limit is ' + audioAttachmentUploader.validateSize + 'mb');
                                    attachment.val('');
                                } else {
                                    var allowed_ext = ['mp3', 'wav','MP3','WAV'];
                                    var extension = attachment.val().substr(attachment.val().length - 3);
                                    if (!!(allowed_ext.indexOf(extension) + 1)) {
                                        audioAttachmentUploader.uploadAudioButton.text('Uploading..').parent('a').hide();
                                        audioAttachmentUploader.uploadingContainer.show();
                                    } else {
                                        alert(extension + ' files are not allowed to be uploaded as audio. Please upload a mp3 or wav file.');
                                        attachment.val('');
                                    }

                                }
                            } else {
                                alert('Please select an audio first');
                            }
                        },
                        onLoad: function () {
                            audioAttachmentUploader.setAudioUploadButton(this);
                        }
                    },
                    {
                        type: 'html',
                        html: '<img class="uploading-img" src="' + audioAttachmentUploader.uploadingSource + '"></img>',
                        style: 'margin-left:35%',
                        hidden: true,
                        onLoad: function () {
                            audioAttachmentUploader.setUploadingContainer(this);
                        }
                    },
                    {
                        type: 'html',
                        html: '<div class="status-message"></div>',
                        style: 'margin-left:32%;  color: green',
                        hidden: true,
                        onLoad: function () {
                            audioAttachmentUploader.setStatusMessageContainer(this);
                        }
                    }
                ]
            },
        ],
        onOk: function (event) {
            if (audioAttachmentUploader.uploadAudioButton.text() != 'Uploaded') {
                if (!confirm('Please make sure you send files to server or else upload will be cancelled!!')) {
                    event.preventDefault();
                }
            } else {
                var url = audioAttachmentUploader.getResultantHTML();
                var value = "<audio src='/static/" + url + "' controls></audio>"
                if (editor.mode == 'wysiwyg') {
                    editor.insertHtml(value);
                } else {
                    editor.setMode('wysiwyg', function () {
                        editor.insertHtml(value);
                        editor.setMode('source');
                    });
                }
            }
        },
        onShow: function () {
            //Remove Focus & fix height
            var fileField = audioAttachmentUploader.getFileField().css('outline', 0);
            $('body').find('iframe.cke_dialog_ui_input_file').css('height', '100px');

            if (audioAttachmentUploader.uploadAudioButton) {
                audioAttachmentUploader.uploadAudioButton.text('Upload audio').parent('a').show();
            }
            //bindUploadEvent only if not binded before
            if (!audioAttachmentUploader.uploadEventBinded) {
                audioAttachmentUploader.bindUploadEvent();
            }
            audioAttachmentUploader.statusMessageContainer.setText('');
            audioAttachmentUploader.statusMessageContainer.hide();

            //setCustomConfiguration
            audioAttachmentUploader.autoClose = audioAttachmentUploader.editor.config.autoCloseUpload || false;
            audioAttachmentUploader.validateSize = audioAttachmentUploader.editor.config.validateSize || 0;
        }
    }
});

CKEDITOR.plugins.add('attach_audio',
    {
        init: function (editor) {
            audioAttachmentUploader.editor = editor;
            editor.ui.addButton('AudioAttachments',
                {
                    label: 'Attach audio files',
                    command: 'OpenAudioWindow',
                    icon: CKEDITOR.plugins.getPath('attach_audio') + 'attach.png'
                });
            var cmd = editor.addCommand('OpenAudioWindow', new CKEDITOR.dialogCommand('abbrDialogsAudio'));
        }
    });