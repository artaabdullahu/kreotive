/*
 Author - Sahil Batla
 Contact - sahilbathla1@gmail.com
 Description - This plugins provides a basic iframe to upload attachments
 Configs while using in editor -
 1) AutoClose -  To auto close dialog on upload (autoClose: true)
 2) Callback on attachment upload - onAttachmentUpload: function() {}
 3) validateSize - Validate size of file before upload (validateSize: 30) i.e 30mb limit
 */
attachAttachmentUploader = {
    uploadButton: null,
    editor: null,
    uploadEventBinded: false,
    uploadingContainer: null,
    statusMessageContainer: null,
    uploadingSource: CKEDITOR.plugins.getPath('attach_attachment') + 'uploading.gif',
    autoClose: false,
    validateSize: 0,
    setStatusMessageContainer: function (_this) {
        this.statusMessageContainer = _this.getElement();
    },
    setUploadingContainer: function (_this) {
        this.uploadingContainer = _this.getElement()
    },
    setuploadButton: function (_this) {
        this.uploadButton = $(_this.getInputElement().$.children[0]);
    },
    getFileField: function () {
        return $($('body').find('iframe.cke_dialog_ui_input_file:visible').contents().find('input[type="file"]'));
    },
    getResultantHTML: function () {
        return $($('body').find('iframe.cke_dialog_ui_input_file:visible').contents().find('body')).text();
    },
    bindUploadEvent: function () {
        //Handle iframe redirect
        var uploadHandler = function () {
            if (attachAttachmentUploader.uploadButton.text() == 'Uploading..') {
                //Provide onAttachmentUpload Callback after upload
                //Define this function in CKEDITOR config
                if (attachAttachmentUploader.editor.config.onVideoAttachmentUpload) {
                    attachAttachmentUploader.editor.config.onVideoAttachmentUpload(attachAttachmentUploader.getResultantHTML());
                }
                attachAttachmentUploader.uploadButton.text('Uploaded');
                attachAttachmentUploader.statusMessageContainer.setText('File Upload Successful!!');
                attachAttachmentUploader.statusMessageContainer.show();
                attachAttachmentUploader.uploadingContainer.hide();
                if (attachAttachmentUploader.autoClose) {
                    CKEDITOR.dialog.getCurrent().hide();
                }
            }
        }
        $('body').find('iframe.cke_dialog_ui_input_file').load(uploadHandler);
        attachAttachmentUploader.uploadEventBinded = true;
    }
}

CKEDITOR.dialog.add('abbrDialogAttachment', function (editor) {
    return {
        title: 'Upload Attachment',
        minWidth: 400,
        minHeight: 200,
        contents: [
            {
                id: 'UploadAttachment',
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
                        'for': ['UploadAttachment', 'attachment'],
                        onClick: function () {
                            var attachment = attachAttachmentUploader.getFileField();
                            if (attachment.val()) {
                                if (attachAttachmentUploader.validateSize > 0 && attachment[0].files[0].size > attachAttachmentUploader.validateSize * 1000000) {
                                    alert('File Size Limit is ' + attachAttachmentUploader.validateSize + 'mb');
                                    attachment.val('');
                                } else {

                                    var allowed_ext = ['pdf', 'odt', 'ppt'];
                                    var extension = attachment.val().substr(attachment.val().length - 3);
                                    if (!!(allowed_ext.indexOf(extension) + 1)) {
                                        attachAttachmentUploader.uploadButton.text('Uploading..').parent('a').hide();
                                        attachAttachmentUploader.uploadingContainer.show();
                                    } else {
                                        alert(extension + ' files are not allowed to be uploaded as attachments. Please upload a pdf,ppt or odt file.');
                                        attachment.val('');
                                    }

                                }
                            } else {
                                alert('Please select an attachment first');
                            }
                        },
                        onLoad: function () {
                            attachAttachmentUploader.setuploadButton(this);
                        }
                    },
                    {
                        type: 'html',
                        html: '<img class="uploading-img" src="' + attachAttachmentUploader.uploadingSource + '"></img>',
                        style: 'margin-left:35%',
                        hidden: true,
                        onLoad: function () {
                            attachAttachmentUploader.setUploadingContainer(this);
                        }
                    },
                    {
                        type: 'html',
                        html: '<div class="status-message"></div>',
                        style: 'margin-left:32%;  color: green',
                        hidden: true,
                        onLoad: function () {
                            attachAttachmentUploader.setStatusMessageContainer(this);
                        }
                    }
                ]
            },
        ],
        onOk: function (event) {

            if (attachAttachmentUploader.uploadButton.text() != 'Uploaded') {
                if (!confirm('Please make sure you send files to server or else upload will be cancelled!!')) {
                    event.preventDefault();
                }
            } else {
                var url = attachAttachmentUploader.getResultantHTML();

                var value = "<a class='attach-attachment' href='/static/" + url + "' download> Download </a>"
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
            var fileField = attachAttachmentUploader.getFileField().css('outline', 0);
            $('body').find('iframe.cke_dialog_ui_input_file').css('height', '100px');

            if (attachAttachmentUploader.uploadButton) {
                attachAttachmentUploader.uploadButton.text('Upload attachment').parent('a').show();
            }
            //bindUploadEvent only if not binded before
            if (!attachAttachmentUploader.uploadEventBinded) {
                attachAttachmentUploader.bindUploadEvent();
            }
            attachAttachmentUploader.statusMessageContainer.setText('');
            attachAttachmentUploader.statusMessageContainer.hide();

            //setCustomConfiguration
            attachAttachmentUploader.autoClose = attachAttachmentUploader.editor.config.autoCloseUpload || false;
            attachAttachmentUploader.validateSize = attachAttachmentUploader.editor.config.validateSize || 0;
        }
    }
});

CKEDITOR.plugins.add('attach_attachment',
    {
        init: function (editor) {
            attachAttachmentUploader.editor = editor;
            editor.ui.addButton('AttachAttachments',
                {
                    label: 'Attach attachment files',
                    command: 'OpenAttachmentWindow',
                    icon: CKEDITOR.plugins.getPath('attach_attachment') + 'attach.png'
                });
            editor.addCommand('OpenAttachmentWindow', new CKEDITOR.dialogCommand('abbrDialogAttachment'));
        }
    });