#/usr/bin/jq
# use jq to turn pueue status -j output into grouped counts of states
# requires jq 1.6 or newer
#
# usage: pueue status -j | jq -r -f <path_for_this_script>

# ANSI color functions
def _ansi_bright($c): tostring | "\u001b[\($c);1m\(.)\u001b[0m";
def red:    _ansi_bright(31);
def green:  _ansi_bright(32);
def yellow: _ansi_bright(33);
def cyan:   _ansi_bright(36);
def white:  _ansi_bright(37);

# Main filter
.tasks
| to_entries
| map({
    "status": (
        # turn the status structure into a string with ANSI color applied
        # this uses destructuring with the ?// alternatives operator
        # (requires jq 1.6 or newer)
        .value.status as
            {Done: $done}
        ?// {Stashed: {enqueue_at: $enq}}
        ?// $status
        | if $done then
            $done as
                {Failed: $ferr}
            ?// {FailedToSpawn: $serr}
            ?// $result
            | if $ferr then
                "Failed" | red
            elif $serr then
                "Failed to spawn" | red
            elif $result == "DependencyFailed" then
                "Dependency failed" | red
            else
                $result | green
            end
        elif $status == "Running" then
            "Running" | green
        elif ($status == "Paused" or $status == "Locked") then
            $status | white
        elif $status then
            $status | yellow
        else  # {Stashed: {enque_at: ...}}, but $enq can be null
            "Stashed" | yellow
        end
    ),
    "group": .value.group | cyan
})
| group_by(.)
| map({"group": .[0].group, "status": .[0].status, "count": length})
| group_by(.group)
| map(
    (map("  \(.status): \(.count)") | join("\n")) as $result
    | "\(.[0].group): \(map(.count) | add) tasks\n\($result)"
)
| join("\n\n")
