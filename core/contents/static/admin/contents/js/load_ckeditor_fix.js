/* 
 * Copyright (c) 2009-2014, FEINHEIT GmbH and individual contributors.
 * All rights reserved.
 * 
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 * 
 *     1. Redistributions of source code must retain the above copyright notice,
 *        this list of conditions and the following disclaimer.
 * 
 *     2. Redistributions in binary form must reproduce the above copyright
 *        notice, this list of conditions and the following disclaimer in the
 *        documentation and/or other materials provided with the distribution.
 * 
 *     3. Neither the name of FEINHEIT GmbH nor the names of its contributors
 *        may be used to endorse or promote products derived from this software
 *        without specific prior written permission.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
 * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
 * ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 * /

/* global django, CKEDITOR */
(function($) {
    // Activate and deactivate the CKEDITOR because it does not like
    // getting dragged or its underlying ID changed.
    // The 'data-processed' attribute is set for compatibility with
    // django-ckeditor.
    $(document).on(
        'content-editor:activate',
        function(event, $row, formsetName) {
            $row.find('textarea[data-type=ckeditortype]').each(function() {
                if (this.getAttribute('data-processed') != '1') {
                    this.setAttribute('data-processed', '1')
                    $($(this).data('external-plugin-resources')).each(function(){
                        CKEDITOR.plugins.addExternal(this[0], this[1], this[2]);
                    });
                    CKEDITOR.replace(this.id, $(this).data('config'));
                }
            });
        }
    ).on(
        'content-editor:deactivate',
        function(event, $row, formsetName) {
            $row.find('textarea[data-type=ckeditortype]').each(function() {
                try {
                    CKEDITOR.instances[this.id] && CKEDITOR.instances[this.id].destroy();
                    this.setAttribute('data-processed', '0')
                } catch(err) {}
            });
        }
    );
})(django.jQuery);
