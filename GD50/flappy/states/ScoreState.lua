--[[
    ScoreState Class
    Author: Colton Ogden
    cogden@cs50.harvard.edu

    A simple state used to display the player's score before they
    transition back into the play state. Transitioned to from the
    PlayState when they collide with a Pipe.
]]

ScoreState = Class{__includes = BaseState}

--[[
    When we enter the score state, we expect to receive the score
    from the play state so we know what to render to the State.
]]

local gold = love.graphics.newImage('gold.png')
local silver = love.graphics.newImage('silver.png')
local bronze = love.graphics.newImage('bronze.png')

function ScoreState:enter(params)
    self.score = params.score
end

function ScoreState:update(dt)
    -- go back to play if enter is pressed
    if love.keyboard.wasPressed('enter') or love.keyboard.wasPressed('return') then
        gStateMachine:change('countdown')
    end
end

function ScoreState:render()
    -- simply render the score to the middle of the screen
    love.graphics.setFont(flappyFont)
    love.graphics.printf('Oof! You lost!', 0, 64, VIRTUAL_WIDTH, 'center')

    -- draw medal
    if self.score >= 15 then
        -- draw at 4% scale (my image is large) at a little above the center of the screen
        love.graphics.draw(gold, VIRTUAL_WIDTH / 2 - gold:getWidth() / 10, VIRTUAL_HEIGHT / 2.1 - gold:getHeight() / 10, 0, 0.2, 0.2)
    elseif self.score >= 10 then
        -- draw at 4% scale (my image is large) at a little above the center of the screen
        love.graphics.draw(silver, VIRTUAL_WIDTH / 2 - silver:getWidth() / 10, VIRTUAL_HEIGHT / 2.1 - silver:getHeight() / 10, 0, 0.2, 0.2)
    elseif self.score >= 5 then
        -- draw at 4% scale (my image is large) at a little above the center of the screen
        love.graphics.draw(bronze, VIRTUAL_WIDTH / 2 - bronze:getWidth() / 10, VIRTUAL_HEIGHT / 2.1 - bronze:getHeight() / 10, 0, 0.2, 0.2)
    end

    love.graphics.setFont(mediumFont)
    love.graphics.printf('Score: ' .. tostring(self.score), 0, 100, VIRTUAL_WIDTH, 'center')

    love.graphics.printf('Press Enter to Play Again!', 0, 160, VIRTUAL_WIDTH, 'center')
end