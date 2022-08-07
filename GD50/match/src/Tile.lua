--[[
    GD50
    Match-3 Remake

    -- Tile Class --

    Author: Colton Ogden
    cogden@cs50.harvard.edu

    The individual tiles that make up our game board. Each Tile can have a
    color and a variety, with the varietes adding extra points to the matches.
]]

Tile = Class{}

function Tile:init(x, y, color, variety)
    -- 1 in 25
    self.shiny = math.random() > 0.96
    
    -- board positions
    self.gridX = x
    self.gridY = y

    -- coordinate positions
    self.x = (self.gridX - 1) * 32
    self.y = (self.gridY - 1) * 32

    -- tile appearance/points
    self.color = color
    self.variety = variety

    if self.shiny then
        self.r, self.g, self.b = math.random(), math.random(), math.random()
        Timer.every(0.3, function()
            self.r = math.random()
            self.g = math.random()
            self.b = math.random()
        end)
    end
end

function Tile:render(x, y)
    if not self.shiny then
        -- draw shadow (looks bad with glaze)
        love.graphics.setColor(34/255, 32/255, 52/255, 1)
        love.graphics.draw(gTextures['main'], gFrames['tiles'][self.color][self.variety],
            self.x + x + 2, self.y + y + 2)
    end

    -- draw tile itself
    love.graphics.setColor(1, 1, 1, 1)
    love.graphics.draw(gTextures['main'], gFrames['tiles'][self.color][self.variety],
        self.x + x, self.y + y)

    if self.shiny then
        -- colorful glaze with rounded edges
        -- (any more opaque and it is hard to tell original color)
        love.graphics.setColor(self.r, self.g, self.b, 65/255)
        love.graphics.rectangle('fill', self.x + x, self.y + y, 32, 32, 8)  
        love.graphics.setColor(1, 1, 1, 1)          
    end
end