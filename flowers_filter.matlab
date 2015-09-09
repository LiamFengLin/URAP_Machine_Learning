% parameters
DIR_PATH = '~/Desktop/flowers/';
OUTPUT_DIR_PATH = '~/Desktop/flowers/filtered/';
REMOVE_PIXELS_LESS_THAN = 30;
FILL_GAPS_PIXELS = 8;
ROUNDNESS_THRESHOLD = 0.5;
files = dir(DIR_PATH);
N = numel(files);

for i=4:N
    RGB=imread([DIR_PATH files(i).name]);
    I = rgb2gray(RGB);
    dims = size(I);
    nRows = dims(1);
    nCols = dims(2);
    left = var(double(I(:,1)'));
    right = var(double(I(:,nCols)'));
    top2Sum = left + right;

    sideColorVar = var(double(I(:,1)') + double(I(:,nCols)'));

    % contrast calculation
    imageArray = reshape(I, 1, []);
    imageContast = var(double(imageArray));

    if ~(top2Sum < 1200 && imageContast > 1000 && sideColorVar < 500)
        continue
    end

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

    [B,L] = bwboundaries(bw,'noholes');

    if (length(B) > 1)
        continue
    end

    boundary = B{1};
    
    stats = regionprops(L,'Area','Centroid');

    % compute a simple estimate of the object's perimeter
    delta_sq = diff(boundary).^2;
    perimeter = sum(sqrt(sum(delta_sq, 2)));

    % obtain the area calculation corresponding to label 'k'
    area = stats(1).Area;

    % compute the roundness metric
    metric = 4 * pi * area / perimeter ^ 2;

    if (metric > ROUNDNESS_THRESHOLD)
        continue
    end

    imwrite(RGB,[OUTPUT_DIR_PATH files(i).name]);
end