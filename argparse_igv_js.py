import sys
import argparse
from os.path import basename
from os.path import isfile

def get_opt():
	group = argparse.ArgumentParser()
	group.add_argument("-r", "--ref", help="reference fasta file", required=True)
	group.add_argument("-m", "--bam", help="Input mapping file, in1.bam in2.bam ...", required=False, nargs = "*")
	
	return group.parse_args()

def build_bam_tracks(bams):
    tracks = []
    for bam in bams:
        if not isfile( bam + ".bai"):
            print("bam file or index file are not existed")
            sys.exit()

        bam_id = basename(bam).replace(".bam","")
        track = """
        {{
            name: "{bam_id}",
            type: "alignment",
            format: "bam",
            url: "{bam}",
            indexURL: "{bam}.bai"
        }},""".format(bam = bam, bam_id = bam_id)
        tracks.append(track)

    tracks = "".join(tracks)[:-1]
    return tracks


def build_ref_track(fasta):
    if not isfile( fasta + ".fai"):
        print("{}.fai is not existed".format(fasta), file=sys.stderr)
        sys.exit()

    genome = basename(fasta)
    genome_id = genome.replace(".fasta","").replace(".fas","").replace(".fa","")

    bam_track ="""genome: "{genome}",
            reference: {{
                id: "{genome_id}",
                fastaURL: "{fasta}",
                indexURL: "{fasta}.fai"
            }}""".format(genome = genome, genome_id = genome_id, fasta = fasta)
    
    return bam_track


def make_html(genome, tracks):
    html = """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>igv.js</title>
   
        <script src="https://igv.org/web/release/2.6.6/dist/igv.min.js"></script>
    </head>
    <body>
        <div id="igv-div"></div>
    </body>
    <script>
        var igvDiv = document.getElementById("igv-div");
        var options = {{
            showNavigation: true,
            showRuler: true,
            {genome},
            tracks: [
                {tracks}
            ]
        }};
    
        igv.createBrowser(igvDiv, options)
            .then(function (browser) {{
                console.log("Created IGV browser");
            }})
    </script>
    </html>""".format(genome = genome, tracks = tracks)
    return html


def igv_web(fasta, bams):

    tracks = ""
    genome_track = build_ref_track(fasta)

    if bams:
        bam_track = build_bam_tracks(bams)
        tracks += bam_track

    html = make_html( genome_track, tracks)

    with open("argparse_index.html", "w") as file:
        file.writelines(html)

if __name__ == "__main__":
     opts = get_opt()
     bams = opts.bam
     fasta = opts.ref
     igv_web(fasta, bams)