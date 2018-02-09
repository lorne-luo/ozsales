"""
Streamfield  definations
"""
from wagtail.wagtailcore.blocks import (CharBlock, ChoiceBlock, RichTextBlock, StreamBlock, StructBlock, TextBlock, PageChooserBlock, ListBlock, RawHTMLBlock)
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock

POSITION_CHOICES = {
    ('left', 'Left'),
    ('center', 'Center'),
}

COLOR_CHOICES = {
    ('purple', 'Purple'),
    ('aqua', 'Aqua'),
    ('navy', 'Navy'),
    ('ice-blue', 'Ice blue'),
    ('violet', 'Violet'),
}

HEADING_SIZE_CHOICES = {
    ('h1', 'H1'),
    ('h2', 'H2'),
    ('h3', 'H3'),
    ('h4', 'H4'),
    ('h5', 'H5')
}


class HeadingBlock(StructBlock):
    class Meta:
        icon = "title"
        template = "blocks/heading_block.html"

    heading_text = CharBlock(classname="Heading", required=True)
    heading_size = ChoiceBlock(choices=HEADING_SIZE_CHOICES, blank=False, required=True)
    heading_position = ChoiceBlock(choices=POSITION_CHOICES, blank=True, required=False, default="left")


class ButtonBlock(StructBlock):
    class Meta:
        icon = "placeholder"
        template = "blocks/button_block.html"

    button_text = CharBlock(required=True)
    link_to_internal_page = PageChooserBlock(can_choose_root=True, required=False)
    link_to_external_page = CharBlock(required=False, help_text="Manually enter URL  if you want the button link to an external page. This value will override the link above.")
    button_color = ChoiceBlock(choices=COLOR_CHOICES, blank=False, required=True)
    button_positon = ChoiceBlock(choices=POSITION_CHOICES, blank=True, required=False, default="left")


class ImageBlock(StructBlock):
    class Meta:
        icon = "image"
        template = "blocks/image_block.html"

    image = ImageChooserBlock()
    image_position = ChoiceBlock(choices=POSITION_CHOICES, blank=True, required=False, default="left")


class EmbedBlock(StructBlock):
    class Meta:
        icon = "media"
        template = "blocks/embed_block.html"

    embed = EmbedBlock()


class AccordionBlock(StructBlock):
    class Meta:
        icon = "arrow-down-big"
        template = "blocks/accordion_block.html"

    accordion_group_title = TextBlock(required=False, blank=True, default="")
    accordion_items = ListBlock(
        StructBlock(
            [
                ('accordion_title', CharBlock(required=True)),
                ('accordion_content', RichTextBlock(required=True)),
            ]
        )
    )


# Define the custom blocks that `StreamField` will utilize
class BaseStreamBlock(StreamBlock):
    heading_block = HeadingBlock()
    button_block = ButtonBlock()
    image_block = ImageBlock()
    accordion_block = AccordionBlock()
    embed_block = EmbedBlock()
    unorderd_list_block = ListBlock((RichTextBlock(label="Unordered list item")), template="blocks/unorderd_list_block.html", icon="list-ul")
    orderd_list_block = ListBlock((RichTextBlock(label="Ordered list item")), template="blocks/orderd_list_block.html", icon="list-ol")
    rich_text_block = RichTextBlock()
    raw_html_block = RawHTMLBlock()
