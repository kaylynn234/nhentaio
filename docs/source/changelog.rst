Changelog
==========

Nhentio's changelog can be found here.
While some versions may not have a changelog entry, significant versions with major or breaking changes will.

0.3.0
------
- Added this changelog since it's become a necessity.
- Due to misconceptions about how nhentai titles worked, things have moved around a bit in this version.
  :attr:`Gallery.title_untranslated` is now :attr:`~.Gallery.subtitle`. Note that the parameter is now `Optional` - meaning it may be ``None``.
  While this is a breaking change in technicality, I don't feel like a new major version is warranted since this doesn't change the way
  you interact with the library in a meaningful way. Version guarantees will come later when I feel the library is in a better state.
  I am aware this technically breaks semvar. I am sorry.
