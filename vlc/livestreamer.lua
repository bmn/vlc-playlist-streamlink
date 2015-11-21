--[[
	Livestreamer playlist plugin by bmn.
	Requires a running livestreamersrv instance on port 10088.
		<https://github.com/athoik/livestreamersrv> by athoik
--]]

function probe()
    if vlc.access ~= "http" and vlc.access ~= "https" then
        return false
    end
    activate = string.match( string.sub( vlc.path, 1, 7 ), "twitch" ) or string.find( vlc.path, ".twitch.tv" )
			or string.match( string.sub( vlc.path, 1, 7 ), "hitbox" ) or string.find( vlc.path, ".hitbox.tv" )
	return activate
end

function parse()
	return {{ path = 'http://127.0.0.1:10088/' .. vlc.path, title = vlc.access .. '://' .. vlc.path }}
end
