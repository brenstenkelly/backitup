// fastscore.recordsets.0: true

#include "fastscore.h"

#include <string.h>
#include <stdlib.h>

void begin()
{
}

int compare(const void *va, const void *vb)
{
    const fastscore_value_t *a = va;
    const fastscore_value_t *b = vb;
    json_t *o1 = json_object_get(a->js, "o");
    json_t *o2 = json_object_get(b->js, "o");
    return json_integer_value(o1) - json_integer_value(o2);
}

void action(fastscore_value_t v, int slot, int seqno)
{
    qsort(v.rs, v.count, sizeof(fastscore_value_t), compare);

    for (int i = 0; i < v.count; i++)
    {
        json_t *bar = v.rs[i].js;
        json_t *foo = json_object_get(bar, "foo");
        const char *str = json_string_value(foo);

        fastscore_emit((fastscore_value_t) {
            .fmt = FASTSCORE_FMT_UTF8,
            .str = strdup(str),
        }, 1);
    }
}

void end1()
{
}

