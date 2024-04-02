from plone.restapi.blocks import iter_block_transform_handlers
from plone.restapi.blocks import visit_blocks


def fix_footer_top_blocks(context, blocks, transformer):
    if not blocks:
        return blocks
    for block in visit_blocks(context, blocks):
        new_block = block.copy()
        for handler in iter_block_transform_handlers(context, block, transformer):
            new_block = handler(new_block)
        block.clear()
        block.update(new_block)
    return blocks
