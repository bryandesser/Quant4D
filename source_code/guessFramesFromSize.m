function guessFramesFromSize(app)
    % Make an initial guess at the file dimensions (assume ~square field of
    % view: ImportFramesX≈ImportFramesY)
    %
    % Parameters:
    %    app: Quant4D class
    %
    % Returns:
    %    None

    if app.ImportPixelsX.Value > 1 && app.ImportPixelsY.Value > 1
        x = sqrt((app.tmp_variables.FileSize-app.DataOffset.Value-app.tmp_variables.fileTail) ...
            /(app.ImportPixelsX.Value*app.ImportPixelsY.Value*app.byte_size.(app.ImportDataType.Value)+app.FrameHeader.Value+app.FrameFooter.Value));
    
        set([app.ImportFramesX, ...
            app.ImportFramesY], ...
            "Value",max(floor(x),1))
    end
end