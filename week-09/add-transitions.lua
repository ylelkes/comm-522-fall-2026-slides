-- Append a transition line to each slide's speaker notes, naming the next slide.
function Pandoc(doc)
  local titles, n = {}, 0
  for _, block in ipairs(doc.blocks) do
    if block.t == "Header" and block.level == 2 then titles[#titles + 1] = pandoc.utils.stringify(block.content) end
  end
  for _, block in ipairs(doc.blocks) do
    if block.t == "Header" and block.level == 2 then
      n = n + 1
    elseif block.t == "Div" and block.classes:includes("notes") then
      local next_title = titles[n + 1]
      if next_title then
        block.content:insert(pandoc.Para({pandoc.Strong("Transition: "), pandoc.Str("next, " .. next_title)}))
      else
        block.content:insert(pandoc.Para({pandoc.Strong("Close: "), pandoc.Str("Pause for final questions and collect the exit response.")}))
      end
    end
  end
  return doc
end
