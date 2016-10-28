/*
 Author - Sahil Batla
 Contact - sahilbathla1@gmail.com
 Description - This plugins provides a basic iframe to upload attachments
 Configs while using in editor -
 1) AutoClose -  To auto close dialog on upload (autoClose: true)
 2) Callback on attachment upload - onAttachmentUpload: function() {}
 3) validateSize - Validate size of file before upload (validateSize: 30) i.e 30mb limit
 */
pictureAttachmentUploader = {
    uploadButton: null,
    editor: null,
    uploadEventBinded: false,
    uploadingContainer: null,
    statusMessageContainer: null,
    uploadingSource: CKEDITOR.plugins.getPath('attach_picture') + 'uploading.gif',
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
            if (pictureAttachmentUploader.uploadButton.text() == 'Uploading..') {
                //Provide onAttachmentUpload Callback after upload
                //Define this function in CKEDITOR config
                if (pictureAttachmentUploader.editor.config.onPictureAttachmentUpload) {
                    pictureAttachmentUploader.editor.config.onPictureAttachmentUpload(pictureAttachmentUploader.getResultantHTML());
                }
                pictureAttachmentUploader.uploadButton.text('Uploaded');
                pictureAttachmentUploader.statusMessageContainer.setText('File Upload Successful!!');
                pictureAttachmentUploader.statusMessageContainer.show();
                pictureAttachmentUploader.uploadingContainer.hide();
                if (pictureAttachmentUploader.autoClose) {
                    CKEDITOR.dialog.getCurrent().hide();
                }
            }
        }
        $('body').find('iframe.cke_dialog_ui_input_file').load(uploadHandler);
        pictureAttachmentUploader.uploadEventBinded = true;
    }
}

CKEDITOR.dialog.add('abbrDialogPicture', function (editor) {
    return {
        title: 'Upload Picture',
        minWidth: 400,
        minHeight: 200,
        contents: [
            {
                id: 'UploadPicture',
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
                        'for': ['UploadPicture', 'attachment'],
                        onClick: function () {
                            var attachment = pictureAttachmentUploader.getFileField();
                            if (attachment.val()) {
                                if (pictureAttachmentUploader.validateSize > 0 && attachment[0].files[0].size > pictureAttachmentUploader.validateSize * 1000000) {
                                    alert('File Size Limit is ' + pictureAttachmentUploader.validateSize + 'mb');
                                    attachment.val('');
                                } else {
                                    pictureAttachmentUploader.uploadButton.text('Uploading..').parent('a').hide();
                                    pictureAttachmentUploader.uploadingContainer.show();
                                }
                            } else {
                                alert('Please select a picture first');
                            }
                        },
                        onLoad: function () {
                            pictureAttachmentUploader.setuploadButton(this);
                        }
                    },
                    {
                        type: 'html',
                        html: '<img class="uploading-img" src="' + pictureAttachmentUploader.uploadingSource + '"></img>',
                        style: 'margin-left:35%',
                        hidden: true,
                        onLoad: function () {
                            pictureAttachmentUploader.setUploadingContainer(this);
                        }
                    },
                    {
                        type: 'html',
                        html: '<div class="status-message"></div>',
                        style: 'margin-left:32%;  color: green',
                        hidden: true,
                        onLoad: function () {
                            pictureAttachmentUploader.setStatusMessageContainer(this);
                        }
                    }
                ]
            },
        ],
        onOk: function (event) {

            if (pictureAttachmentUploader.uploadButton.text() != 'Uploaded') {
                if (!confirm('Please make sure you send files to server or else upload will be cancelled!!')) {
                    event.preventDefault();
                }
            } else {
                var url = pictureAttachmentUploader.getResultantHTML();
                var value = "<img src='/static/" + url + "' width='100%' ></img>"
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
            var fileField = pictureAttachmentUploader.getFileField().css('outline', 0);
            $('body').find('iframe.cke_dialog_ui_input_file').css('height', '100px');

            if (pictureAttachmentUploader.uploadButton) {
                pictureAttachmentUploader.uploadButton.text('Upload attachment').parent('a').show();
            }
            //bindUploadEvent only if not binded before
            if (!pictureAttachmentUploader.uploadEventBinded) {
                pictureAttachmentUploader.bindUploadEvent();
            }
            pictureAttachmentUploader.statusMessageContainer.setText('');
            pictureAttachmentUploader.statusMessageContainer.hide();

            //setCustomConfiguration
            pictureAttachmentUploader.autoClose = pictureAttachmentUploader.editor.config.autoCloseUpload || false;
            pictureAttachmentUploader.validateSize = pictureAttachmentUploader.editor.config.validateSize || 0;
        }
    }
});

CKEDITOR.plugins.add('attach_picture',
    {
        init: function (editor) {
            pictureAttachmentUploader.editor = editor;
            editor.ui.addButton('PictureAttachments',
                {
                    label: 'Attach picture files',
                    command: 'OpenPictureWindow',
                    icon: CKEDITOR.plugins.getPath('attach_picture') + 'attach.png'
                });
            editor.addCommand('OpenPictureWindow', new CKEDITOR.dialogCommand('abbrDialogPicture'));
        }
    });