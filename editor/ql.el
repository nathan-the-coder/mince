;;; mylsl-mode.el --- sample major mode for editing LSL. -*- coding: utf-8; lexical-binding: t; -*-

;; Copyright © 2017, by you

;; Author: your name ( your email )
;; Version: 2.0.13
;; Created: 26 Jun 2015
;; Keywords: languages
;; Homepage: http://ergoemacs.org/emacs/elisp_syntax_coloring.html

;; This file is not part of GNU Emacs.

;;; License:

;; You can redistribute this program and/or modify it under the terms of the GNU General Public License version 2.

;;; Commentary:

;; short description here

;; full doc on how to use here

;;; Code:

;; create the list for font-lock.
;; each category of keyword is given a particular face
(setq ql-font-lock-keywords
      (let* (
            ;; define several category of keywords
            (x-keywords '("BREAK" "EXIT" "ELSE" "IF" "RETURN" "WHILE"))
            (x-constants '("DEFINE" "INIT" "RUN" "FORMAT" "OUTPUT"))
            (x-functions '("SERVE" "INPUT"))

            ;; generate regex string for each category of keywords
            (x-keywords-regexp (regexp-opt x-keywords 'words))
            (x-constants-regexp (regexp-opt x-constants 'words))
            (x-functions-regexp (regexp-opt x-functions 'words)))

        `(
          (,x-constants-regexp . 'font-lock-constant-face)
          (,x-functions-regexp . 'font-lock-function-name-face)
          (,x-keywords-regexp . 'font-lock-keyword-face)
          ;; note: order above matters, because once colored, that part won't change.
          ;; in general, put longer words first
          )))

;;;###autoload
(define-derived-mode ql-mode c-mode "ql-mode"
  "Major mode for editing Ql Language…"

  ;; code for syntax highlighting
  (setq font-lock-defaults '((ql-font-lock-keywords))))

;; add the mode to the `features' list
(provide 'ql-mode)

;;; ql.el ends here
