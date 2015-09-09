% perimeter toggles
REMOVE_PIXELS_LESS_THAN = 300;
FILL_GAPS_PIXELS = 20;

DIR_PATH = '~/Desktop/flowers/withbackground/';
files = dir(DIR_PATH);
N = numel(files);
a = [];
for i=3:N
    try
        RGB=imread([DIR_PATH files(i).name]);
        I = rgb2gray(RGB);
        threshold = graythresh(I);
        bw = im2bw(I,threshold);
        dims = size(I);
        nRows = dims(1);
        nCols = dims(2);
        left = bw(:,1)';
        right = bw(:,nCols)';
        top = bw(1,:);
        bottom = bw(nRows,:);
        total = cat(2, left, right, top, bottom);
        boundaryPercentWhite = sum(total) / length(total);
        if boundaryPercentWhite > 0.4
          bw = ~bw;
        end  

        % remove all object containing fewer than 30 pixels
        bw = bwareaopen(bw, REMOVE_PIXELS_LESS_THAN);

        % fill gaps within boundary
        se = strel('disk', FILL_GAPS_PIXELS);
        % morphological close operation
        bw = imclose(bw,se);

        % fill any holes, so that regionprops can be used to estimate
        % the area enclosed by each of the boundaries
        bw = imfill(bw,'holes');

        for r = 1:nRows
            for c = 1:nCols
                if bw(r, c) == 0
                    RGB(r, c, :) = [0,0,0];
                end
            end
        end

        imwrite(RGB,['~/Desktop/flowers/strippedbackground/' files(i).name]);

        percentCore = sum(sum(bw)) / nRows / nCols;
        a = [a, percentCore];
    catch 
    end
end

% for testing

RGB=imread('test_image4.jpg');
I = rgb2gray(RGB);
threshold = graythresh(I);
bw = im2bw(I,threshold);
dims = size(I);
nRows = dims(1);
nCols = dims(2);
left = bw(:,1)';
right = bw(:,nCols)';
top = bw(1,:);
bottom = bw(nRows,:);
total = cat(2, left, right, top, bottom);
boundaryPercentWhite = sum(total) / length(total);
if boundaryPercentWhite > 0.4 
  bw = ~bw;
end  

% remove all object containing fewer than 30 pixels
bw = bwareaopen(bw, REMOVE_PIXELS_LESS_THAN);

% fill gaps within boundary
se = strel('disk', FILL_GAPS_PIXELS);
% morphological close operation
bw = imclose(bw,se);

% fill any holes, so that regionprops can be used to estimate
% the area enclosed by each of the boundaries
bw = imfill(bw,'holes');

for r = 1:nRows
    for c = 1:nCols
        if bw(r, c) == 0
            RGB(r, c, :) = [0,0,0];
        end
    end
end

percentCore = sum(sum(bw)) / nRows / nCols;
imshow(RGB)