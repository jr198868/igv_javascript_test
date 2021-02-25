import sys
import argparse
import os
from os.path import basename


def build_bam_tracks(bams, bam_index):
    tracks = []
    bam_id = basename(bams).replace(".bam","")
    print(bams)
    track = """
        {{
            name: "{}",
            type: "alignment",
            format: "bam",
            url: "{}",
            indexURL: "{}"
        }},""".format(bam_id, bams, bam_index)
    tracks.append(track)

    tracks = "".join(tracks)[:-1]
    return tracks


def build_ref_track(fasta):

    genome = basename(fasta)
    genome_id = genome.replace(".fasta","").replace(".fas","").replace(".fa","")

    bam_track ="""genome: "{}",
            reference: {{
                id: "{}",
                fastaURL: "{}",
                indexURL: "{}.fai"
            }}""".format(genome, genome_id, fasta, fasta)

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


def igv_web(fasta, bams, bam_index):

    tracks = ""
    genome_track = build_ref_track(fasta)

    if bams:
        bam_track = build_bam_tracks(bams, bam_index)
        tracks += bam_track

    html = make_html(genome_track, tracks)

    with open("igv_index.html", "w") as file:
        file.writelines(html)


if __name__ == "__main__":
    bam_path = '/Users/ranjing/Desktop/'
    fasta_path = '/Users/ranjing/Desktop/iMiHA/application/files/reference/'
    
    bams = '{}wgEncodeUwRepliSeqBjS1AlnRep1.bam'.format(bam_path)
    bam_index = '{}wgEncodeUwRepliSeqBjS1AlnRep1.bam.bai'.format(bam_path)

    fasta = '{}b37decoy.fasta'.format(fasta_path)
    fasta_index = '{}b37decoy.fasta.fai'.format(fasta_path)
    igv_web(fasta, bams, bam_index)

    