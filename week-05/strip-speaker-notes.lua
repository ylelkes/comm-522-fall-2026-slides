-- Remove speaker-note content from the student deck before HTML is written.
function Div(el)
  if el.classes:includes("notes") then
    return {}
  end
end
